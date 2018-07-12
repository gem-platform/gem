def permissions_required(permissions):
    def real_decorator(function):
        def wrapper(context, sid, data):
            user = context.get_user(sid)
            if not user:
                return {"success": False, "message": "Wrong session token"}

            for permission in permissions:
                if not user.have_permission(permission):
                    return {"success": False, "message": "Insufficient rights"}
            return function(context, sid, data)
        return wrapper
    return real_decorator
