#!/usr/local/bin/python3

from os import environ

from datetime import datetime, timedelta

from jinja2 import Environment, FileSystemLoader

from gem.db import Meeting
from gem.utils.db import connect_db
from gem.postman import Postman

connect_db()
postman = Postman("info@gem.iskcon.com")
postman.connect(
    environ.get("SMTP_HOST", "postman"),
    environ.get("SMTP_PORT", 25)
)
jinja = Environment(
    loader=FileSystemLoader("templates")
)
#jinja.filters["days"] = days
template_html = jinja.get_template("action_required.html.jinja2")
template_plain = jinja.get_template("action_required.plain.jinja2")

now = datetime.now()
already_done = [] # todo: load from disk


# def days(start, end):
#     return timedelta(start, end).days

def event_id(meeting, event):
    return "{}-{}".format(meeting.id, event)


for meeting in Meeting.objects.all():
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

    # filter out events that have already been reported
    days_to_send = {event: date for event, date in days.items()
                    if date <= now and event_id(meeting, event) not in already_done}

    # send emails
    for event, date in days_to_send.items():
        for user in users:
            msg_plain = template_plain.render(event=event, user=user, meeting=meeting)
            msg_html = template_html.render(event=event, user=user, meeting=meeting)
            postman.send(user.email, "Meeting Notification", msg_html, msg_plain)
