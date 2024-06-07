from users.models import User
from users.selectors import filter_users


class UserSerializer:
    def __init__(self, instance=None | User, data=None | dict) -> None:
        self.instance = instance
        self.data = data

    def validate(self):
        if self.data:
            username = self.data["username"]
            if len(username) > 100:
                raise ValueError("username -> username must be less than 100 char")
            if not any(letter.isupper() for letter in username):
                raise ValueError("username -> username must contain uppercase char")
            if not any(letter.islower() for letter in username):
                raise ValueError("username -> username must contain lowercase char")
            if not any(letter.isdigit() for letter in username):
                raise ValueError("username -> username must contain numbers")
            if filter_users(username=username).first() is not None:
                raise ValueError("username -> this username already exists")

    def data(self) -> dict:
        if self.instance is not None:
            user = {
                "id": self.instance.id,
                "username": self.instance.username,
                "email": self.instance.email,
                "phone": self.instance.phone,
                "birthday": str(self.instance.birthday),
                "created_at": str(self.instance.created_at),
            }
            return user
        else:
            return None
