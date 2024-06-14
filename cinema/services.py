from datetime import datetime

from sqlalchemy.orm import Session

from cinema.models import Cinema, Showtime, ShowtimeSeats, Subscription
from cinema.selectors import get_cinema
from movie.services import get_or_create_movie
from source.database import DatabaseConnection
from users.models import User


def add_cinema(
    *,
    name: str,
    ticket_price: int,
    capacity: int,
    number_of_row: int,
    number_of_col: int,
) -> Cinema:
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
            capacity=cinema.capacity,
        )
        for col in range(cinema.number_of_col):
            for row in range(cinema.number_of_row):
                seat = ShowtimeSeats(
                    row=row,
                    col=col,
                    showtime=showtime,
                )
                session.add(seat)
        session.add(showtime)
        session.commit()


def reserve_seat(user_id: int, seat_id: int):
    session = Session(DatabaseConnection.engin)
    try:
        query = (
            session.query(ShowtimeSeats, Cinema.ticket_price, Showtime)
            .select_from(ShowtimeSeats)
            .join(Showtime, ShowtimeSeats.showtime_id == Showtime.id)
            .join(Cinema, Showtime.cinema_id == Cinema.id)
            .filter(ShowtimeSeats.id == seat_id)
            .with_for_update()
            .one()
        )
        seat = query[0]
        if seat.is_reserved == True:
            raise ValueError("this seat is taken befor")
        ticket_price = query[1]
        showtime = query[2]

        # Start a transaction

        user = session.query(User).filter(User.id == user_id).with_for_update().one()
        subscription = (
            session.query(Subscription)
            .filter(Subscription.user_id == user_id)
            .with_for_update()
            .one()
        )

        discount = 0
        price = ticket_price

        if subscription.credit > 0:
            if subscription.type_subscription.name == "silver":
                discount += 0.2 * price
                subscription.credit -= 1
            elif subscription.type_subscription.name == "gold":
                discount += 0.5 * price
                subscription.credit -= 1
            elif (
                datetime.date().month == datetime(user.birthday).month
                and datetime.date().day == datetime(user.birthday).day
            ):
                discount += 0.5 * price

        final_price = price - discount
        if user.wallet >= final_price:
            user.wallet -= final_price
            seat.money_spent = final_price
            seat.reserved_by = user
            seat.is_reserved = True
            showtime.capacity -= 1
        else:
            raise ValueError("insufficient funds")

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def cancel_reserved_seat(user_id: int, seat_id: int):
    session = Session(DatabaseConnection.engin)
    try:
        query = (
            session.query(ShowtimeSeats, Showtime)
            .select_from(ShowtimeSeats)
            .join(Showtime, ShowtimeSeats.showtime_id == Showtime.id)
            .filter(ShowtimeSeats.id == seat_id)
            .with_for_update()
            .one()
        )
        seat = query[0]

        if seat.is_reserved == False:
            raise ValueError("this seat is not reserved")
        if seat.reserved_by_id != user_id:
            raise ValueError("you are not owner of this seat")

        showtime = query[1]

        # Start a transaction

        user = session.query(User).filter(User.id == user_id).with_for_update().one()

        price = 0
        if (showtime.show_time - datetime.now()).total_seconds() > 3600:
            price = seat.money_spent
        elif showtime.show_time > datetime.now():
            price = seat.money_spent * 0.82

        seat.money_spent = None
        user.wallet += price
        showtime.capacity += 1
        seat.reserved_by = None
        seat.is_reserved = False

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
