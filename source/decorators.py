from datetime import datetime

from source.authentication import is_admin, is_authenticate, is_owner
from source.wsgi import WSGIHandler


def auth_requirement(view):
    def wrapper(*args, **kwargs):
        if is_authenticate(request=args[0]):
            return view(*args, **kwargs)
        else:
            return WSGIHandler.response_access_denied_not_auth(*args)

    return wrapper


def owner_requirement(view):
    def wrapper(*args, **kwargs):
        if is_owner(request=args[0], id=kwargs["user_id"]) is not None:
            return view(*args, **kwargs)
        else:
            return WSGIHandler.response_access_denied_not_owner(*args)

    return wrapper


def admin_requirement(view):
    def wrapper(*args, **kwargs):
        if is_admin(*args, **kwargs):
            return view(*args, **kwargs)
        else:
            return WSGIHandler.response_access_denied_not_admin(*args)

    return wrapper


def allowed_methods(methods: list):
    def dec_method(view):
        def wrapper(*args, **kwargs):
            if args[0].method in methods:
                return view(*args, **kwargs)
            else:
                return WSGIHandler.response_method_not_allowed(*args)

        return wrapper

    return dec_method


def tracker(view):
    def wrapper(*args, **kwargs):
        f = open("./logs/cinema.log", "a")
        f.write(f"\n\n----- new request ----- {datetime.now()}\n\n")
        f.write(f"[request]: \n{args[0]}")
        response = view(*args, **kwargs)
        f.write(f"\n\n[response]:\n {response}")
        f.write(f"\n\n----- end request ----- {datetime.now()}\n\n")
        f.close()
        return response

    return wrapper
