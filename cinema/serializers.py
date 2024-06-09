from cinema.models import Cinema
from cinema.selectors import filter_cinemas


class CinemaSerializer:
    def __init__(self, instance: Cinema | None = None, data: dict | None = None) -> None:
        self.instance = instance
        self.data = data

    def validate(self):
        if self.data:
            name = self.data['name']
            ticket_price = self.data['ticket_price']
            capacity = self.data['capacity']
            number_of_row = self.data['number_of_row']
            number_of_col = self.data['number_of_col']

            if name:
                if filter_cinemas(name = name).first() is not None:
                    raise ValueError('name -> this name already exists')

            if ticket_price:
                if ticket_price < 0:
                    raise ValueError('ticket_price must be greater than 0')

            if capacity and number_of_row and number_of_col:
                if capacity != number_of_row * number_of_col:
                    raise ValueError('capacity does not match with number of rows and number of columns')

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