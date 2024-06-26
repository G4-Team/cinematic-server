from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.query import Query

from cinema.models import Subscription
from movie.models import MovieReview
from source.database import DatabaseConnection
from users.models import User


def get_user(id: id) -> User:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(User).options(joinedload(User.subscription))
        user = query.get(id)
    return user


def filter_users(**kwargs) -> Query:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(User)
        users = query.filter_by(**kwargs)
    return users
