import jwt
from webob import Request

from settings.base import JWT_SECRET
from users.selectors import get_user


def is_authenticate(request: Request):
    token = request.cookies.get("jwt")

    if not token:
        return False

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms="HS256")
    except Exception:
        return False

    user = get_user(id=payload["id"])
    if user is None:
        return False

    return True


def is_admin(request: Request):
    token = request.cookies.get("jwt")

    if not token:
        return False

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms="HS256")
    except Exception:
        return False

    user = get_user(id=payload["id"])
    if user is None:
        return False
    if user.is_admin is False:
        return False

    return True
