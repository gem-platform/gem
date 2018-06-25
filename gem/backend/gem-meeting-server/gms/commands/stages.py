# Acquaintance Stage


def reading_progress(context, sid, data):
    """Update reading progress of proposal."""
    quantity = data.get("quantity", 0)  # progress (from 0 to 1)
    user = context.get_user(sid)
    context.stage.set_progress(user, quantity)
    return {"success": True}

# Ballot Stage


def vote(context, sid, data):
    """User vote message received."""
    user = context.get_user(sid)
    value = data.get("value", None)

    # check user rights
    if not user.have_permission("meeting.vote"):
        return {"success": False, "message": "Insufficient rights"}

    # commit a vote
    context.stage.vote(user, value)
    return {"success": True}


def ballot_secret(context, sid, data):
    """Change ballot secret."""
    user = context.get_user(sid)
    value = data.get("value", None)

    # check user rights
    if not user.have_permission("meeting.manage"):
        return {"success": False, "message": "Insufficient rights"}

    # update ballot secret state
    context.stage.ballot.secret = value
    return {"success": True, "value": context.stage.ballot.secret}

# Comments Stage


def comment(context, sid, data):
    """Comment received."""
    user = context.get_user(sid)
    message = data.get("message", None)
    mark = data.get("mark", None)

    # check user rights
    if not user.have_permission("meeting.manage"):
        return {"success": False, "message": "Insufficient rights"}

    # commit comment
    context.stage.comment(user, message, mark)
    return {"success": True}

# Discussion Stage


def request_floor(context, sid, data):
    """Request floor."""
    user = context.get_user(sid)

    # check user rights
    if not user.have_permission("meeting.discuss"):
        return {"success": False, "message": "Insufficient rights"}

    # request floor
    context.stage.request_floor(user)
    return {"success": True}


def withdraw_from_queue(context, sid, data):
    """Withdraw from queue."""
    user = context.get_user(sid)

    # check user rights
    if not user.have_permission("meeting.discuss"):
        return {"success": False, "message": "Insufficient rights"}

    # withdraw from queue
    context.stage.withdraw_from_queue(user)
    return {"success": True}


def remove_from_queue(context, sid, data):
    """Remove from queue."""
    user = context.get_user(sid)
    user_id_to_remove = data.get("id", None)
    user_to_remove = context.get_user_by_id(user_id_to_remove)

    # check user rights
    if not user.have_permission("meeting.manage"):
        return {"success": False, "message": "Insufficient rights"}

    # withdraw from queue
    context.stage.withdraw_from_queue(user_to_remove)
    return {"success": True}


def give_voice(context, sid, data):
    """Give voice to specified user at discussion stage."""
    user = context.get_user(sid)
    give_voice_to = data.get("to", None)
    user_to_give_voice = context.get_user_by_id(give_voice_to)

    # check user rights
    if not user.have_permission("meeting.manage"):
        return {"success": False, "message": "Insufficient rights"}

    # give voice
    context.stage.give_voice(user_to_give_voice)
    return {"success": True}

# General


def switch_stage(context, sid, data):
    """Switch stage request received."""
    index = data.get("index", None)
    user = context.get_user(sid)

    # check user rights
    if not user.have_permission("meeting.manage"):
        return {"success": False, "message": "Insufficient rights"}

    # change stage
    context.meeting.stages.switch_to(index)
    return {"success": True}


def close(context, sid, data):
    """Close meeting"""
    user = context.get_user(sid)

    # check user rights
    if not user.have_permission("meeting.manage"):
        return {"success": False, "message": "Insufficient rights"}

    # close meeting
    context.send_broadcast("close", {})
    return {"success": True}


def stage_timer(context, sid, data):
    """Add time for stage"""
    user = context.get_user(sid)

    # check user rights
    if not user.have_permission("meeting.manage"):
        return {"success": False, "message": "Insufficient rights"}

    context.send_broadcast("stage_timer", data)
    return {"success": True}


# Info

def user_inactive(context, sid, data):
    """User away from keyboard"""
    user = context.get_user(sid)
    value = data.get("value", False)
    context.set_user_inactivity_status(user, value)
    context.send_broadcast("inactive_users", context.inactive_users)
    return {"success": True}


def meeting_users_online(context, sid, data):
    ids = list(map(lambda u: str(u.id), context.sessions.online))
    return {"success": True, "online": ids}