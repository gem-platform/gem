def permissions_required(permissions):
    def real_decorator(function):
        def wrapper(meeting, sid, data):
            user = meeting.get_user(sid)
            if not user:
                return {"success": False, "message": "Wrong session token"}

            for permission in permissions:
                if not user.have_permission(permission):
                    return {"success": False, "message": "Insufficient rights"}
            return function(meeting, sid, data)
        return wrapper
    return real_decorator
