from source.database import DatabaseConnection
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from cinema.models import Cinema


def get_cinema(id: id) -> Cinema:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(Cinema)
        cinema = query.get(id)
    return cinema


def filter_cinemas(**kwargs) -> Query:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(Cinema)
        cinemas = query.filter_by(**kwargs)
    return cinemas
