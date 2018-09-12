"""Handshake command handlers."""

from logging import getLogger
from gms.net.serializers.meeting import MeetingSerializer

LOG = getLogger("handlers")


def connect(context, sid, environ):
    """New client connected to server."""
    # new socket connection received
    # with specified session id (sid)
    # todo: add to "spectators" list
    # todo: to observe connected but not authenticated
    # todo: users (for security reasons)
    LOG.info("Client %s connected", sid)


def disconnect(context, sid):
    """Client disconnected from server."""
    # socket connection with specified
    # session id is closed
    # todo: remove from "spectators" list (if present)
    LOG.info("Client %s disconnected", sid)
    context.logout_user(sid)


def handshake(context, sid, data):
    """Handshake message received."""
    LOG.info("Handshake received from '%s'", sid)

    # find user using specified credentials
    token = data.get("token", None)
    user = context.get_user_by_token(token)

    # no user found using specified credentails
    # send response with meaningful info
    if not user:
        return {"success": False, "message": "Wrong access token"}

    # no meeting found (wrong ID, exception while loading meeting)
    if not context.meeting:
        return {"success": False, "message": "Meeting not found"}

    # user found by specified credentials, so login
    # him by associating sessionId (sid) with model (user)
    context.login_user(sid, user)

    # serialize whole meeting state and return
    # it as response to the "handshake" request
    serializer = MeetingSerializer()
    meeting_state = serializer.serialize(context.meeting)

    # send response
    return {
        "success": True,
        "message": "Welcome, {}!".format(user.name),
        "state": meeting_state,
        "user": {
            "id": str(user.id),
            "name": user.name,
            "permissions": user.permissions
        }
    }
