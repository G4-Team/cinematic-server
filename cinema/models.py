import enum
from datetime import datetime

import sqlalchemy as db
from sqlalchemy import Enum

from source.model import Base


class Cinema(Base):
    __tablename__ = "cinemas"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    number_of_row = db.Column(db.Integer, nullable=False)
    number_of_col = db.Column(db.Integer, nullable=False)
    show_times = db.orm.relationship("Showtime", back_populates="cinema")


class Showtime(Base):
    __tablename__ = "showtimes"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    show_time = db.Column(db.DateTime, nullable=False)
    seats = db.orm.relationship("ShowtimeSeats", back_populates="showtime")
    cinema_id = db.orm.mapped_column(db.ForeignKey("cinemas.id"), nullable=False)
    cinema = db.orm.relationship("Cinema", back_populates="show_times")
    movie_id = db.orm.mapped_column(db.ForeignKey("movies.id"), nullable=False)
    movie = db.orm.relationship("Movie", back_populates="show_times")


class ShowtimeSeats(Base):
    __tablename__ = "showtime_seats"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    showtime_id = db.orm.mapped_column(db.ForeignKey("showtimes.id"), nullable=False)
    showtime = db.orm.relationship("Showtime", back_populates="seats")
    is_reserved = db.Column(db.Boolean, nullable=False, default=False)
    reserved_by_id = db.orm.mapped_column(db.ForeignKey("users.id"), nullable=False)
    reserved_by = db.orm.relationship("User", back_populates="reservations")
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)


class SubscriptionType(enum.Enum):
    bronze = 0
    silver = 3
    gold = 6


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = db.Column(
        db.BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    type_subscription = db.Column(Enum(SubscriptionType))

    validity_duration = db.Column(
        db.SmallInteger,
        nullable=True,
    )
    price = db.Column(
        db.Float,
        nullable=False,
    )
    credit = db.Column(
        db.SmallInteger,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(),
    )

    user_id = db.orm.mapped_column(
        db.ForeignKey("users.id"),
        nullable=False,
    )
    user = db.orm.relationship(
        "User",
        back_populates="subscription",
    )
