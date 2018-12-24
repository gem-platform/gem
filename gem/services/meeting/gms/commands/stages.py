"""Meeting command handlers."""

from ._aux import permissions_required

# Acquaintance Stage


def reading_progress(meeting, sid, data):
    """Update reading progress of proposal."""
    quantity = data.get("quantity", 0)  # progress (from 0 to 1)
    user = meeting.get_user(sid)
    meeting.stage.set_progress(user, quantity)
    return {"success": True}


# Ballot Stage

@permissions_required(["meeting.vote"])
def vote(meeting, sid, data):
    """User vote message received."""
    user = meeting.get_user(sid)
    value = data.get("value", None)
    result = meeting.stage.vote(user, value)
    return {"success": result[0], "message": result[1]}


@permissions_required(["meeting.manage"])
def ballot_secret(meeting, sid, data):
    """Change ballot secret."""
    value = data.get("value", None)
    meeting.stage.ballot.secret = value
    return {"success": True}


@permissions_required(["meeting.manage"])
def ballot_threshold(meeting, sid, data):
    """Change ballot threshold."""
    value = float(data.get("value", None))
    meeting.stage.ballot.threshold = value
    return {"success": True}

# Comments Stage

@permissions_required(["meeting.comment"])
def comment(meeting, sid, data):
    """Comment received."""
    user = meeting.get_user(sid)
    message = data.get("message", None)
    mark = data.get("mark", None)
    quote = data.get("quote", None)
    meeting.stage.comment(user, message, mark, quote)
    return {"success": True}


# Discussion Stage

@permissions_required(["meeting.discuss"])
def request_floor(meeting, sid, data):
    """Request the floor."""
    user = meeting.get_user(sid)
    meeting.stage.request_floor(user)
    return {"success": True}


@permissions_required(["meeting.discuss"])
def withdraw_from_queue(meeting, sid, data):
    """Withdraw from queue."""
    user = meeting.get_user(sid)
    meeting.stage.withdraw_from_queue(user)
    return {"success": True}


@permissions_required(["meeting.manage"])
def remove_from_queue(meeting, sid, data):
    """Remove from queue."""
    user_id_to_remove = data.get("id", None)
    user_to_remove = meeting.get_user_by_id(user_id_to_remove)
    meeting.stage.withdraw_from_queue(user_to_remove)
    return {"success": True}


@permissions_required(["meeting.manage"])
def give_voice(meeting, sid, data):
    """Give voice to specified user at discussion stage."""
    give_voice_to = data.get("to", None)
    user_to_give_voice = meeting.get_user_by_id(give_voice_to)
    meeting.stage.give_voice(user_to_give_voice)
    return {"success": True}


# General

@permissions_required(["meeting.manage"])
def switch_stage(meeting, sid, data):
    """Switch stage request received."""
    index = data.get("index", None)
    meeting.stages.switch_to(index)
    return {"success": True}


@permissions_required(["meeting.manage"])
def close(meeting, sid, data):
    """Close meeting"""
    meeting.send("close", {})
    meeting.sessions.delete_all()
    meeting.close_meeting()
    return {"success": True}


@permissions_required(["meeting.manage"])
def stage_timer(meeting, sid, data):
    """Add time for stage."""
    meeting.send("stage_timer", data)
    return {"success": True}


@permissions_required(["meeting.manage"])
def request_quick_ballot(meeting, sid, data):
    """Create new quick ballot."""
    meeting.quick_ballot.start_new()
    meeting.send("quick_ballot", data)
    return {"success": True}


def quick_ballot_vote(meeting, sid, data):
    """Commit a vote for quick ballot."""
    value = data.get("vote", None)
    results = meeting.quick_ballot.vote(value)
    online_users_count = len(meeting.sessions.online)
    meeting.send("quick_ballot_results", {
        "results": results,
        "online_count": online_users_count
    })
    return {"success": True}


@permissions_required(["meeting.manage"])
def request_quorum_change(meeting, sid, data):
    """Change quorum request received."""
    value = int(data.get("value", None))
    users_can_change = meeting.quorum.users_can_change
    names = list(map(lambda x: x.name, users_can_change))

    # get online of users who can change a quorum
    users = list(filter(lambda user: user in meeting.sessions.online,
                        users_can_change))

    # qourom not met
    if len(users) < len(users_can_change):
        return {
            "success": False,
            "users": names,
            "message": "Only {} of {} GBC EC members present"
                       .format(len(users), len(users_can_change))
        }

    # send for each allowed user
    for user in users:
        session_id = meeting.sessions.get_session(user)
        meeting.send("quorum_change", {
            "value": value, "stage": "request"
        }, to=session_id)

    # request change
    meeting.quorum.request_change(value)

    # success
    return {"success": True}


@permissions_required(["meeting.quorum_change"])
def vote_quorum_change(meeting, sid, data):
    """Commit a vote for change a quorum."""
    value = data.get("value", None)
    user = meeting.get_user(sid)
    managers = filter(lambda user: user.have_permission("meeting.manage") or
                      user.have_permission("meeting.quorum_change"),
                      meeting.sessions.online)

    # commit a vote
    result = meeting.quorum.vote_change(user, value)
    br = result.value  # ballot result

    # quorum change is approved -> notify users
    for user in managers:
        session_id = meeting.sessions.get_session(user)
        meeting.send("quorum_change", {
            "value": meeting.quorum.value,
            "stage": "final" if br is True else \
                    "failed" if br is False else \
                    "progress"
        }, to=session_id)

    return {"success": True}

# Info

def user_inactive(meeting, sid, data):
    """User away from keyboard."""
    user = meeting.get_user(sid)
    if not user:
        return {"success": False}

    value = data.get("value", False)
    meeting.sessions.meta.set(user, "inactive", value)
    return {"success": True}
