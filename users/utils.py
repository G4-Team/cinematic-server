import hashlib

import jwt

from settings.base import JWT_SECRET, SALT_SECRET


def creat_jwt_token(user_id) -> str:
    payload = dict(
        id=user_id,
    )
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return token


def hash_password(password: str) -> str:
    password = password + SALT_SECRET
    hash_password = hashlib.md5(password.encode())

    return hash_password.hexdigest()
