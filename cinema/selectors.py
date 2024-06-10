from sqlalchemy import select
from source.database import DatabaseConnection
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.orm.query import Query
from cinema.models import Cinema, Showtime
from ..movie.models import Movie


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

def get_movie_showtimes(movie_id: int) -> Query:
    stmt = (
        select(Showtime, Cinema, Movie)
        .options(selectinload(Showtime.cinema, Showtime.movie))
        .where(Showtime.movie_id == movie_id)
        .join(Movie)
        .join(Cinema)
    )
    result = []
    with Session(DatabaseConnection.engin) as session:
        for row in session.execute(stmt):
            result.append(row[0])
    return result

def get_cinema_showtimes(cinema_id: int) -> Query:
    stmt = (
        select(Showtime, Cinema, Movie)
        .options(selectinload(Showtime.cinema, Showtime.movie))
        .where(Showtime.cinema_id == cinema_id)
        .join(Cinema)
        .join(Moive)
    )
    result = []
    with Session(DatabaseConnection.engin) as session:
        for row in session.execute(stmt):
            result.append(row[0])
    return result