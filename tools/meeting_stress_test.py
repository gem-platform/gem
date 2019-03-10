import random
import time
import socketio
from loremipsum import get_sentences
from mongoengine import connect
from gem.db import Ballot, User


sockets = []
HOST = "gemapp.in"
MEETING_TO_JOIN = "5c821fab52974a000873b11c"
LAST_STAGE = "@LAST"
CURRENT_STAGE = ""
READING_PROGRESS = 0


connect("gem",
        host=HOST, username="bhagavan",
        password="UZz5dGzZn@R*jj9%",
        authentication_source="admin",
        authentication_mechanism="SCRAM-SHA-1")


def on_connect():
    pass


def on_handshake_handler(data):
    print(data['success'], data['message'])


def on_stage_switched(data):
    global CURRENT_STAGE
    CURRENT_STAGE = data['state']['type']

def on_vote(data):
    print(data)

def on_comment(data):
    print(data)

# @sio.on('message')
# def on_message(data):
#     print('I received a message!')

# @sio.on('disconnect')
# def on_disconnect():
#     print('I\'m disconnected!')


users = User.objects.all()[:25]
for user in users:
    sio = socketio.Client()
    sockets.append(sio)
    time.sleep(.5)

    sio.on('connect', on_connect)
    sio.on('stage_switched', on_stage_switched)
    sio.connect('https://' + HOST + '/socket.io')
    sio.emit('handshake', {'token': str(user.id), 'meeting': MEETING_TO_JOIN}, callback=on_handshake_handler)


while True:
    if LAST_STAGE != CURRENT_STAGE:
        LAST_STAGE = CURRENT_STAGE

    print(CURRENT_STAGE)
    for s in sockets:
        time.sleep(.3)
        if CURRENT_STAGE in ["BallotStage", "FeedbackStage"]:
            value = random.choice(['yes', 'no', 'abstained'])
            s.emit("vote", {"value": value}, callback=on_vote)
            print("-> Vote: ", value)

        if CURRENT_STAGE in ["CommentsStage", "FeedbackStage"]:
            should_i_comment = random.randint(1, 20)
            if should_i_comment != 2:
                continue

            mark = random.choice(['+', '-', 'i'])
            sentenses = random.randint(1, 5)
            message = " ".join(get_sentences(sentenses))
            s.emit("comment", {"message": message, "mark": mark}, callback=on_comment)
            print("-> Comment: ", mark, message)

        if CURRENT_STAGE in ["FeedbackStage"]:
            READING_PROGRESS += 1
            s.emit("reading_progress", {"quantity": READING_PROGRESS / 500}, callback=on_comment)

print("done")
