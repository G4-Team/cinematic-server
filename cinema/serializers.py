import re

from cinema.models import Cinema, Showtime, ShowtimeSeats
from cinema.selectors import filter_cinemas


class CinemaSerializer:
    def __init__(
        self, instance: Cinema | None = None, data: dict | None = None
    ) -> None:
        self.instance = instance
        self.data = data

    def validate(self):
        if self.data:
            name = self.data["name"]
            ticket_price = self.data["ticket_price"]
            capacity = self.data["capacity"]
            number_of_row = self.data["number_of_row"]
            number_of_col = self.data["number_of_col"]

            if name:
                if filter_cinemas(name=name).first() is not None:
                    raise ValueError("name -> this name already exists")

            if ticket_price:
                if ticket_price < 0:
                    raise ValueError("ticket_price must be greater than 0")

            if capacity and number_of_row and number_of_col:
                if capacity != number_of_row * number_of_col:
                    raise ValueError(
                        "capacity does not match with number of rows and number of columns"
                    )

    @property
    def serialized_data(self):
        if self.instance is not None:
            cinema = {
                "id": self.instance.id,
                "name": self.instance.name,
                "ticket_price": self.instance.ticket_price,
                "capacity": self.instance.capacity,
                "number_of_row": self.instance.number_of_row,
                "number_of_col": self.instance.number_of_col,
            }
            return cinema
        else:
            return None


class ShowtimeSerializer:
    def __init__(
        self, instance: Showtime | None = None, data: dict | None = None
    ) -> None:
        self.instance = instance
        self.data = data

    def validate(self):
        if self.data:
            time = self.data["time"]
            if not re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}", time):
                raise ValueError("time invalid. default time format yyyy-mm-dd hh:mm")

    @property
    def serialized_data(self) -> dict:
        if self.instance is not None:
            showtime = {
                "id": self.instance.id,
                "time": str(self.instance.show_time),
                "cinema": {
                    "name": self.instance.cinema.name,
                    "ticket_price": self.instance.cinema.ticket_price,
                },
                "movie": {
                    "name": self.instance.movie.name,
                    "age-rating": self.instance.movie.age_rating,
                },
                "capacity": self.instance.capacity,
            }
            return showtime
        else:
            return None


class ShowtimeSeatSerializer:
    def __init__(
        self, instance: ShowtimeSeats | None = None, data: dict | None = None
    ) -> None:
        self.instance = instance
        self.data = data

    def validate(self):
        pass

    @property
    def serialized_data(self) -> dict:
        if self.instance is not None:
            showtime_seat = {
                "id": self.instance.id,
                "row": self.instance.row,
                "col": self.instance.col,
                "is_reserved": self.instance.is_reserved,
                "reserved_by": self.instance.reserved_by_id,
                "showtime_id": self.instance.showtime.id,
            }
            return showtime_seat
        else:
            return None
