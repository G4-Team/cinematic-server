from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from movie.models import Movie, MovieReview
from source.database import DatabaseConnection


def get_movie(id: id) -> Movie:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(Movie)
        movie = query.get(id)
    return movie


def filter_movie(**kwargs) -> Query:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(Movie)
        movies = query.filter_by(**kwargs)
    return movies


def dfs_comments_to_dict(comment: MovieReview):
    replies = dict()
    for reply in comment.replies:
        replies[reply.id] = {
            "text": reply.text,
            "rate": reply.rate,
        }
        if reply.replies:
            replies[reply.id]["replies"] = dfs_comments_to_dict(reply)
    return replies


def list_commets(movie_id: int) -> dict:
    with Session(DatabaseConnection.engin) as session:
        root_comments = (
            session.query(MovieReview)
            .filter(MovieReview.reply_to == None, MovieReview.movie_id == movie_id)
            .all()
        )
        all_comments_dict = dict()
        for comment in root_comments:
            all_comments_dict[comment.id] = {
                'id': comment.id,
                "text": comment.text,
                "rate": comment.rate,
            }
            if comment.replies:
                all_comments_dict[comment.id]["replies"] = dfs_comments_to_dict(comment)
        return all_comments_dict

