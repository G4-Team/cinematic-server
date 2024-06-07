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
