from movie.models import Movie, MovieReview
from movie.selectors import filter_movie


class MovieSerializer:
    def __init__(self, instance=None | Movie, data=None | dict, partial=False) -> None:
        self.instance = instance
        self.data = data
        self.partial = partial

    def validate(self):
        if self.data:
            name = self.data["name"]
            if filter_movie(name=name).first():
                raise ValueError("this film already exists")

    @property
    def serialized_data(self) -> dict:
        if self.instance is not None:
            movie = {
                "id": self.instance.id,
                "name": self.instance.name,
                "avg_rates": self.instance.avg_rates,
            }
            return movie
        else:
            return None


class MovieReviewSerializer:
    def __init__(
        self, instance=None | MovieReview, data=None | dict, partial=False
    ) -> None:
        self.instance = instance
        self.data = data
        self.partial = partial

    def validate(self):
        pass

    @property
    def serialized_data(self) -> dict:
        if self.instance is not None:
            movie = {
                "id": self.instance.id,
                "text": self.instance.text,
                "user_id": self.instance.user_id,
                "movie_id": self.instance.movie_id,
            }
            if self.instance.rate:
                movie["rate"] = self.instance.rate

            return movie
        else:
            return None
