from datetime import datetime

import sqlalchemy as db

from source.model import Base


class User(Base):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    username = db.Column(
        db.String(100),
        unique=True,
        nullable=True,
    )
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
    )
    phone = db.Column(
        db.String(11),
        nullable=True,
    )
    password = db.Column(
        db.String(255),
        nullable=False,
    )
    birthday = db.Column(
        db.DATE,
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.now(),
        nullable=False,
    )
    is_admin = db.Column(
        db.Boolean,
        default=False,
    )
    last_login = db.Column(
        db.DateTime,
        nullable=True,
    )

    wallet = db.Column(
        db.Float,
        default=0,
        nullable=False,
    )
    bank_account = db.orm.relationship(
        "BankAccount",
        back_populates="user",
    )
    movie_reviews = db.orm.relationship(
        "MovieReview",
        back_populates="user",
    )
    reservations = db.orm.relationship(
        "ShowtimeSeats",
        back_populates="reserved_by",
    )
