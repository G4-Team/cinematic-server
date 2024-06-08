import jwt

from settings.base import JWT_SECRET


def creat_jwt_token(user_id) -> str:
    payload = dict(
        id=user_id,
    )
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return token
