import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.orm.query import Query

from cinema.models import Cinema, Showtime, ShowtimeSeats
from movie.models import Movie
from source.database import DatabaseConnection
from users.models import User


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


def filter_showtimes(**kwargs) -> Query:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(Showtime)
        showtimes = query.filter_by(**kwargs)
    return showtimes


def get_all_showtimes() -> list:
    stmt = (
        select(Showtime, Cinema, Movie)
        .options(selectinload(Showtime.cinema), selectinload(Showtime.movie))
        .join(Movie)
        .join(Cinema)
    )
    result = []

    with Session(DatabaseConnection.engin) as session:
        for row in session.execute(stmt).all():
            result.append(row[0])
    result = sorted(result, key=lambda x: x.movie.show_times)
    return result


def get_showtimes(user: User) -> list:
    age = (datetime.datetime.now().date() - user.birthday).days / 365
    stmt = (
        select(Showtime, Cinema, Movie)
        .options(selectinload(Showtime.cinema), selectinload(Showtime.movie))
        .where(
            Showtime.show_time > datetime.datetime.now(),
            Movie.age_rating <= age,
            Showtime.capacity > 0,
        )
        .join(Movie)
        .join(Cinema)
    )
    result = []

    with Session(DatabaseConnection.engin) as session:
        for row in session.execute(stmt).all():
            result.append(row[0])
    result = sorted(result, key=lambda x: x.movie.avg_rates, reverse=True)
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
        .options(selectinload(ShowtimeSeats.showtime))
        .where(ShowtimeSeats.showtime_id == showtime_id)
        .join(Showtime)
    )
    with Session(DatabaseConnection.engin) as session:
        seats = session.execute(stmt).all()
    return seats


def get_reservations(user_id: int) -> list:
    stmt = (
        select(ShowtimeSeats, Showtime.id)
        .options(selectinload(ShowtimeSeats.showtime))
        .where(ShowtimeSeats.reserved_by_id == user_id)
        .join(Showtime)
    )
    with Session(DatabaseConnection.engin) as session:
        reservations = session.execute(stmt).all()
    return reservations
