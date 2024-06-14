from sqlalchemy import select, update
from sqlalchemy.orm import Session

from movie.models import Movie, MovieReview
from source.database import DatabaseConnection
from users.models import User
from users.selectors import get_user


def get_movie_review(id: int) -> MovieReview:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(MovieReview)
        return query.get(id)


def get_movie(id: int) -> Movie:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(Movie)
        return query.get(id)


def add_movie(*, name: str):
    with Session(DatabaseConnection.engin) as session:
        movie = Movie(name=name)
        session.add(movie)
        session.commit()
        return session.query(Movie).get(movie.id)


def add_movie_review(*, rate: float, text: str, user_id: int, movie_id: int):
    user = get_user(user_id)
    movie = get_movie(movie_id)
    with Session(DatabaseConnection.engin) as session:
        stmt = select(MovieReview.id).where(MovieReview.movie_id == movie.id)
        befor_reviews_count = len(session.execute(stmt).all())
        new_avg_rate = ((befor_reviews_count * movie.avg_rates) + rate) / (
            befor_reviews_count + 1
        )

        review = MovieReview(
            rate=rate,
            text=text,
            user=user,
            movie=movie,
        )
        stmt2 = update(Movie).values(avg_rates=new_avg_rate).where(Movie.id == 1)
        with DatabaseConnection.engin.begin() as conn:
            conn.execute(statement=stmt2)
        session.add(review)
        session.commit()
        return session.query(MovieReview).get(review.id)


def add_comment_movie_review(*, text: str, user_id: int, review_id: int):
    review = get_movie_review(review_id)
    user = get_user(user_id)

    with Session(DatabaseConnection.engin) as session:
        comment = MovieReview(
            text=text,
            user=user,
            movie=get_movie(review.movie_id),
            reply_to=review,
        )

        session.add(comment)
        session.commit()
        return session.query(MovieReview).get(comment.id)


def get_or_create_movie(name: str, age_rating: int) -> Movie:
    with Session(DatabaseConnection.engin) as session:
        movie = session.query(Movie).filter_by(name=name, age_rating=age_rating).first()

        if movie is None:
            movie = Movie(name=name, age_rating=age_rating)
            session.add(movie)
            session.commit()

    return movie
