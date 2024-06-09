from sqlalchemy.orm import Session

from movie.models import Movie
from source.database import DatabaseConnection


def add_movie(*, name: str):
    with Session(DatabaseConnection.engin) as session:
        movie = Movie(name=name)
        session.add(movie)
        session.commit()
