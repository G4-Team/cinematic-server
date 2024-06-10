from source.database import DatabaseConnection
from sqlalchemy.orm import Session

from cinema.models import Cinema


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