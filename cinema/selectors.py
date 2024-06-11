from sqlalchemy import select
from source.database import DatabaseConnection
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.orm.query import Query
from cinema.models import Cinema, Showtime, ShowtimeSeats
from ..movie.models import Movie
from datetime import datetime


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


def get_showtimes() -> list:
    stmt = (
        select(Showtime, Cinema, Movie)
        .options(selectinload(Showtime.cinema, Showtime.movie))
        .where(Showtime.show_time > datetime.now())
        .join(Movie)
        .join(Cinema)
    )
    result = []
    with Session(DatabaseConnection.engin) as session:
        for row in session.execute(stmt):
            result.append(row[0])
    return result

def get_movie_showtimes(movie_id: int) -> list:
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

def get_cinema_showtimes(cinema_id: int) -> list:
    stmt = (
        select(Showtime, Cinema, Movie)
        .options(selectinload(Showtime.cinema, Showtime.movie))
        .where(Showtime.cinema_id == cinema_id)
        .join(Movie)
        .join(Cinema)
    )
    result = []
    with Session(DatabaseConnection.engin) as session:
        for row in session.execute(stmt):
            result.append(row[0])
    return result

def get_showtime_seats(showtime_id: int) -> list:
    stmt = (
        select(ShowtimeSeats)
        .where(ShowtimeSeats.showtime_id == showtime_id)
    )
    result = []
    with Session(DatabaseConnection.engin) as session:
        for row in session.execute(stmt):
            result.append(row[0])
    return result