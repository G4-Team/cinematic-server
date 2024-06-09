from movie.models import Movie
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
