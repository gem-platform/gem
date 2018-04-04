def have_read(context, sid, data):
    return {"success": True}


def switch_stage(context, sid, data):
    """Switch stage request received."""
    index = data.get("index", None)
    context.meeting.stages.switch_to(index)
    return {"success": True}


def vote(context, sid, data):
    """User vote message received."""
    user = context.get_user(sid)
    value = data.get("value", None)
    context.stage.vote(user, value)
    return {"success": True}


def comment(context, sid, data):
    """Comment received."""
    user = context.get_user(sid)
    message = data.get("message", None)
    mark = data.get("mark", None)
    context.stage.comment(user, message, mark)
    return {"success": True}


def request_floor(context, sid, data):
    """Request floor."""
    user = context.get_user(sid)
    context.stage.request_floor(user)
    return {"success": True}


def withdraw_from_queue(context, sid, data):
    """Withdraw from queue."""
    user = context.get_user(sid)
    context.stage.withdraw_from_queue(user)
    return {"success": True}


def remove_from_queue(context, sid, data):
    """Remove from queue."""
    # todo: sid have enought rights
    user_id_to_remove = data.get("id", None)
    user = context.get_user_by_id(user_id_to_remove)
    context.stage.withdraw_from_queue(user)
    return {"success": True}


def give_voice(context, sid, data):
    """Give voice to specified user at discussion stage."""
    # todo; sid have enought rights
    give_voice_to = data.get("to", None)
    user = context.get_user_by_id(give_voice_to)
    context.stage.give_voice(user)
    return {"success": True}
    # return {"success": False, "message": "Discussion is closed"}
