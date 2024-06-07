from sqlalchemy.orm import Session

from source.database import DatabaseConnection
from users.models import User


def add_user(
    *, username: str, email: str, phone=None | str, password: str, birthday: str
) -> None:
    session = Session(DatabaseConnection.engin)
    user = User(
        username=username,
        email=email,
        password=password,
        birthday=birthday,
    )
    session.add(user)
    session.commit()
