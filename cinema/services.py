from source.database import DatabaseConnection
from sqlalchemy.orm import Session

from cinema.models import Cinema, Showtime


def add_cinema(
    *, name: str, ticket_price: int, capacity: int, number_of_row: int, number_of_col: int
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
        *, show_time: str, cinema_id: int, movie_id: int
) -> None:
    with Session(DatabaseConnection.engin) as session:
        showtime = Showtime(
            show_time=show_time,
            cinema_id=cinema_id,
            movie_id=movie_id,
        )
        session.add(showtime)
        session.commit()