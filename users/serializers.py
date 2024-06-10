import re

from users.models import User
from users.selectors import filter_users


class UserSerializer:
    def __init__(self, instance=None | User, data=None | dict, partial=False) -> None:
        self.instance = instance
        self.data = data
        self.partial = partial

    def validate(self):
        if self.data:
            if self.partial is False:
                username = self.data["username"]
                email = self.data["email"]
                phone = self.data.get("phone", None)
                password = self.data["password"]
                birthday = self.data["birthday"]
            else:
                username = self.data.get("username", None)
                email = self.data.get("email", None)
                phone = self.data.get("phone", None)
                password = self.data.get("password", None)
                birthday = self.data.get("birthday", None)

            if username:
                if len(username) > 100:
                    raise ValueError("username -> username must be less than 100 char")
                if any(not letter.isalnum() for letter in username):
                    raise ValueError("username -> username must contain only alphanumeric chars")
                if filter_users(username=username).first() is not None:
                    raise ValueError("username -> this username already exists")

            if email:
                if not re.fullmatch(
                    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", email
                ):
                    raise ValueError("email -> email not valid")
                if filter_users(email=email).first() is not None:
                    raise ValueError("email -> this email already exists")

            if phone:
                if len(phone) != 11 or not phone.startswith("09"):
                    raise ValueError("phone -> phone not valid")

            if password:
                if len(password) < 8:
                    raise ValueError(
                        "password -> password must contain at least 8 char"
                    )
                if len({x for x in password if x in "$&#@"}) < 2:
                    raise ValueError(
                        "password -> password must contain at least two characters from #$@&"
                    )

                allowed_pattern = re.compile(r"^[A-Za-z0-9@#$&]+$")
                if not allowed_pattern.match(password):
                    raise ValueError(
                        "password -> password contains invalid characters. Only letters, numbers, and @#$& are allowed"
                    )

            if birthday:
                if not re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}").match(birthday):
                    raise ValueError("birthday -> birthday is invalid")
                if int(birthday.split("-")[0]) < 1900:
                    raise ValueError("birthday -> birthday is invalid")

    @property
    def serialized_data(self) -> dict:
        if self.instance is not None:
            user = {
                "id": self.instance.id,
                "username": self.instance.username,
                "email": self.instance.email,
                "phone": self.instance.phone,
                "birthday": str(self.instance.birthday),
                "last_login": str(self.instance.created_at),
                "created_at": str(self.instance.created_at),
                "wallet": self.instance.wallet.balance,
            }
            return user
        else:
            return None
