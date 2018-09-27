"""Meeting command handlers."""

from ._aux import permissions_required

# Acquaintance Stage


def reading_progress(context, sid, data):
    """Update reading progress of proposal."""
    quantity = data.get("quantity", 0)  # progress (from 0 to 1)
    user = context.get_user(sid)
    context.stage.set_progress(user, quantity)
    return {"success": True}


# Ballot Stage

@permissions_required(["meeting.vote"])
def vote(context, sid, data):
    """User vote message received."""
    user = context.get_user(sid)
    value = data.get("value", None)
    result = context.stage.vote(user, value)
    return {"success": result[0], "message": result[1]}


@permissions_required(["meeting.manage"])
def ballot_secret(context, sid, data):
    """Change ballot secret."""
    value = data.get("value", None)
    context.stage.ballot.secret = value
    return {"success": True, "value": context.stage.ballot.secret}


# Comments Stage

@permissions_required(["meeting.comment"])
def comment(context, sid, data):
    """Comment received."""
    user = context.get_user(sid)
    message = data.get("message", None)
    mark = data.get("mark", None)
    context.stage.comment(user, message, mark)
    return {"success": True}


# Discussion Stage

@permissions_required(["meeting.discuss"])
def request_floor(context, sid, data):
    """Request the floor."""
    user = context.get_user(sid)
    context.stage.request_floor(user)
    return {"success": True}


@permissions_required(["meeting.discuss"])
def withdraw_from_queue(context, sid, data):
    """Withdraw from queue."""
    user = context.get_user(sid)
    context.stage.withdraw_from_queue(user)
    return {"success": True}


@permissions_required(["meeting.manage"])
def remove_from_queue(context, sid, data):
    """Remove from queue."""
    user_id_to_remove = data.get("id", None)
    user_to_remove = context.get_user_by_id(user_id_to_remove)
    context.stage.withdraw_from_queue(user_to_remove)
    return {"success": True}


@permissions_required(["meeting.manage"])
def give_voice(context, sid, data):
    """Give voice to specified user at discussion stage."""
    give_voice_to = data.get("to", None)
    user_to_give_voice = context.get_user_by_id(give_voice_to)
    context.stage.give_voice(user_to_give_voice)
    return {"success": True}


# General

@permissions_required(["meeting.manage"])
def switch_stage(context, sid, data):
    """Switch stage request received."""
    index = data.get("index", None)
    context.meeting.stages.switch_to(index)
    return {"success": True}


@permissions_required(["meeting.manage"])
def close(context, sid, data):
    """Close meeting"""
    context.send("close", {})
    context.sessions.delete_all()
    context.close_meeting()
    return {"success": True}


@permissions_required(["meeting.manage"])
def stage_timer(context, sid, data):
    """Add time for stage."""
    context.send("stage_timer", data)
    return {"success": True}


# Info

def user_inactive(context, sid, data):
    """User away from keyboard."""
    user = context.get_user(sid)
    if not user:
        return {"success": False}

    value = data.get("value", False)
    context.sessions.meta.set(user, "inactive", value)
    return {"success": True}
