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

    show_times = db.orm.relationship(
        "Showtime",
        back_populates="movie",
    )


class MovieComment(Base):
    __tablename__ = "movie_comments"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    rate = db.Column(
        db.Float,
        nullable=True,
        default=0,
    )
    text = db.Column(
        db.Text,
        nullable=False,
        default="",
    )

    user_id = db.orm.mapped_column(
        db.ForeignKey("users.id"),
        nullable=False,
    )
    user = db.orm.relationship(
        "User",
        back_populates="movie_comment",
    )

    is_reply = db.Column(
        db.Boolean,
    )
