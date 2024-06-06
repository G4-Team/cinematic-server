from sqlalchemy.orm import Session

from source.database import DatabaseConnection
from users.models import User


def get_user(*, id: int) -> User:
    session = Session(DatabaseConnection.engin)
    query = session.query(User)
    user = query.get(id)

    return user
