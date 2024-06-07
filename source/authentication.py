import jwt

from settings.base import JWT_SECRET
from users.selectors import get_user


def is_authenticate(request):
    token = request.COOKIES.get("jwt")

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
