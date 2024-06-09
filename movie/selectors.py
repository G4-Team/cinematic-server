from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from movie.models import Movie
from source.database import DatabaseConnection


def filter_movie(**kwargs) -> Query:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(Movie)
        movies = query.filter_by(**kwargs)
    return movies
