from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from source.database import DatabaseConnection
from users.models import User


def get_user(id: id) -> User:
    session = Session(DatabaseConnection.engin)
    query = session.query(User)
    user = query.get(id)

    return user


def filter_users(**kwargs) -> Query:
    session = Session(DatabaseConnection.engin)
    query = session.query(User)
    users = query.filter_by(**kwargs)
    return users
