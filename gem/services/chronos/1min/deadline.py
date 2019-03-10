#!/usr/local/bin/python3

"""
Send email notification for GEM Online meetings.
"""

from os import environ
from os.path import exists
from itertools import chain
from datetime import datetime, timedelta
from json import dump as json_dump, load as json_load

from jinja2 import Environment, FileSystemLoader

from gem.db import Meeting
from gem.utils.db import connect_db
from gem.postman import Postman

DONE_PATH = "/usr/app/state/deadline.json"
TEMPLATES_PATH = "/usr/app/templates"
GEM_DOMAIN = environ.get("GEM_DOMAIN", "localhost")
EMAILS_SENT = 0

connect_db()
postman = Postman("info@gemapp.in")
postman.connect(
    environ.get("SMTP_HOST", "postman"),
    environ.get("SMTP_PORT", 25)
)
if environ.get("SMTP_LOGIN"):
    postman.login(
        environ.get("SMTP_LOGIN", "user"),
        environ.get("SMTP_PASSWORD", "pwd")
    )

jinja = Environment(
    loader=FileSystemLoader(TEMPLATES_PATH)
)
template_html = jinja.get_template("action_required.html.jinja2")
template_plain = jinja.get_template("action_required.plain.jinja2")

now = datetime.now()
already_done = [] # todo: load from disk


if exists(DONE_PATH):
    with open(DONE_PATH) as f:
        already_done = json_load(f)


def event_id(meeting, event):
    return "{}-{}".format(meeting.id, event)


def get_values(stage):
    if "progress" not in stage:
        return {}
    if "values" not in stage["progress"]:
        return {}
    return stage["progress"]["values"]


for meeting in Meeting.objects.all():
    # search for a "feedback" stages:
    # 1. get list of actions of proposals for current meeting
    # 2. get list of unique action"s name
    actions = map(lambda p: list(map(lambda a: a.id, p.stage.actions)), meeting.proposals)
    actions = set(list(chain.from_iterable(actions)))
    if "feedback" not in actions:
        continue  # this meeting have no proposals with "feedback" stage

    # calculate days
    days = {}
    span = meeting.end - meeting.start

    # send on a first day of meeting
    if meeting.start:
        days["start"] = meeting.start

    # if meeting is long send on the following days:
    #   - half way to end
    #   - three days before end
    #   - one day before end
    if span.days > 10:
        days["half"] = meeting.start + (span / 2)
        days["dead-3"] = meeting.end - timedelta(days=3)
        days["dead-1"] = meeting.end - timedelta(days=1)

    # get list of users allowed to join meeting
    users = meeting.resolve("meeting.join")
    users_names = list(map(lambda u: u.name, users))

    # filter out events that have already been reported
    days_to_send = {event: date for event, date in days.items()
                    if date <= now and event_id(meeting, event) not in already_done}

    if not days_to_send:
        continue

    # log
    print("Processing '{}':".format(meeting.title))
    print("  State     :", meeting.state)
    print("  Sending to: {}".format(users_names))
    print("  Events    : {}".format(days_to_send))

    # get progress
    stages = list(filter(lambda s: s.stage == "feedback", meeting.state))

    # send emails
    for event, date in days_to_send.items():
        eid = event_id(meeting, event)
        already_done.append(eid)

        for user in users:
            progress = list(map(lambda s: str(get_values(s).get(str(user.id), 0) * 100), stages))
            progress = ", ".join(progress)

            msg_plain = template_plain.render(event=event, user=user, meeting=meeting, progress=progress, domain=GEM_DOMAIN)
            msg_html = template_html.render(event=event, user=user, meeting=meeting, progress=progress, domain=GEM_DOMAIN)
            try:
                if user.email:
                    print("  -> Send : {}".format(user.email))
                    postman.send(user.email, "Meeting Notification", msg_html, msg_plain)
                    EMAILS_SENT += 1
                else:
                    print("  -> Error: {} ({})".format(user.name, "no email"))
            except Exception as ex:
                print("  X Error: ", ex)


# save done events
with open(DONE_PATH, "w+") as outfile:
    json_dump(already_done, outfile)


if EMAILS_SENT > 0:
    print("Emails sent {}".format(EMAILS_SENT))
