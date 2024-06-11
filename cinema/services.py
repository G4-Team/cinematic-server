from sqlalchemy.orm import Session

from cinema.models import Cinema, Showtime
from cinema.selectors import get_cinema
from movie.services import get_or_create_movie
from source.database import DatabaseConnection


def add_cinema(
    *,
    name: str,
    ticket_price: int,
    capacity: int,
    number_of_row: int,
    number_of_col: int,
) -> None:
    with Session(DatabaseConnection.engin) as session:
        cinema = Cinema(
            name=name,
            ticket_price=ticket_price,
            capacity=capacity,
            number_of_row=number_of_row,
            number_of_col=number_of_col,
        )
        session.add(cinema)
        session.commit()


def add_showtime(
    *,
    time: str,
    cinema_id: int,
    movie_name: str,
    movie_age_rating: int,
) -> None:
    with Session(DatabaseConnection.engin) as session:
        cinema = get_cinema(id=cinema_id)
        movie = get_or_create_movie(name=movie_name, age_rating=movie_age_rating)
        showtime = Showtime(
            show_time=time,
            cinema=cinema,
            movie=movie,
        )
        session.add(showtime)
        session.commit()
