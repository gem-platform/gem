"""Handshake command handlers."""

from logging import getLogger
from gms.net.serializers.meeting import MeetingSerializer
from ._aux import permissions_required

LOG = getLogger("meetings")


def connect(meeting, sid, environ):
    """New client connected to server."""
    # new socket connection received
    # with specified session id (sid)
    # todo: add to "spectators" list
    # todo: to observe connected but not authenticated
    # todo: users (for security reasons)
    LOG.info("Client %s connected", sid)


def disconnect(meeting, sid, data=None):
    """Client disconnected from server."""
    # socket connection with specified
    # session id is closed
    # todo: remove from "spectators" list (if present)
    LOG.info("Client %s disconnected", sid)
    meeting.logout_user(sid)


def handshake(meeting, sid, data):
    """Handshake message received."""
    LOG.info("Handshake received from '%s'", sid)

    # find user using specified credentials
    token = data.get("token", None)
    user = meeting.get_user_by_token(token)

    # no user found using specified credentails
    # send response with meaningful info
    if not user:
        return {
            "success": False,
            "message": "You have no rights to join this meeting",
            "actions": ["request_access"]  # provide list of actions user can do
        }

    # no meeting found (wrong ID, exception while loading meeting)
    if not meeting:
        return {"success": False, "message": "Meeting not found"}

    # user found by specified credentials, so login
    # him by associating sessionId (sid) with model (user)
    meeting.login_user(sid, user)

    # serialize whole meeting state and return
    # it as response to the "handshake" request
    serializer = MeetingSerializer()
    meeting_state = serializer.serialize(meeting)

    # send response
    return {
        "success": True,
        "message": "Welcome, {}!".format(user.name),
        "state": meeting_state
    }

def request_access(meeting, sid, data):
    """The user does not have permission to access the meeting,
       and he is requesting access rights."""
    token = data.get("token", None)
    user = meeting.find_user(token)  # todo: change to get_user_by_token
                                     # todo: (with search in list of not allowed users)

    # no user found to grant access to
    if not user:
        return {"success": False, "message": "No user found"}

    # request access
    meeting.sessions.requests.add(sid, user)

    # send response
    return {
        "success": True,
        "message": "Access rights have been requested. " + \
            "Please wait until the secretary accepts your request.",
    }

@permissions_required(["meeting.manage"])
def grant_access(meeting, sid, data):
    """Grant access rights."""
    token = data.get("token", None)
    value = data.get("value", False)
    user = meeting.find_user(token)
    response_sid = meeting.sessions.requests.sid(user)

    # session ID was not found
    if not response_sid:
        return {"success": False, "message": "Session ID was not found"}

    if value:  # access granted
        response = {"success": True, "meeting": meeting.meeting_id, "force": True}
        meeting.allowed_users.append(user)
        meeting.full_sync()
        meeting.send("open_meeting", response, to=response_sid)
    else:  # request was rejected
        response = {"success": False, "message": "Your access request has been rejected"}
        meeting.send("open_meeting", response, to=response_sid)

    return {"success": True}
