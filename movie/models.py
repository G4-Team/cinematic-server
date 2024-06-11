from datetime import datetime

import sqlalchemy as db

from source.model import Base


class Movie(Base):
    __tablename__ = "movies"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
    )
    avg_rates = db.Column(
        db.Float,
        nullable=False,
        default=0,
    )

    movie_reviewes = db.orm.relationship(
        "MovieReview",
        back_populates="movie",
    )

    show_times = db.orm.relationship(
        "Showtime",
        back_populates="movie",
    )


class MovieReview(Base):
    __tablename__ = "movie_reviews"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    rate = db.Column(
        db.Float,
        nullable=True,
    )
    text = db.Column(
        db.Text,
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
        back_populates="movie_reviews",
    )
    movie_id = db.orm.mapped_column(
        db.ForeignKey("movies.id"),
        nullable=False,
    )
    movie = db.orm.relationship(
        "Movie",
        back_populates="movie_reviewes",
    )

    reply_to_id = db.orm.mapped_column(
        db.ForeignKey("movie_reviews.id"),
        nullable=True,
    )
    reply_to = db.orm.relationship(
        "MovieReview",
        remote_side=[id],
        backref="replies",
    )
