from ._aux import permissions_required

@permissions_required(["meeting.manage"])
def force_join(meeting, sid, data):
    # to="connected" will send message to ALL the connected
    # users regardless their connection to meeting
    meeting.send("open_meeting", {
        "meeting": meeting.meeting_id,
        "success": True
    }, to="connected")
    return {"success": True, "message": "All users have been joined a meeting by force"}
