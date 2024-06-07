from users.models import User


def user_serializer(user: User) -> dict:
    user = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "birthday": str(user.birthday),
        "created_at": str(user.created_at),
    }
    return user
