import re

from bank.models import Bank, BankAccount
from bank.selectors import filter_cards
from users.models import User


class CardSerializer:
    def __init__(
        self, instance=None | BankAccount, data=None | dict, partial=False
    ) -> None:
        self.instance = instance
        self.data = data
        self.partial = partial

    def validate(self):
        if self.data:
            card_number = self.data["card_number"]
            if filter_cards(card_number=card_number).first() is not None:
                raise ValueError("card number -> this card number already exists")
            expiration_date = self.data["expiration_date"]
            if not re.match(r"[0-9]{2}-[0-9]{2}", expiration_date):
                raise ValueError("expiration date is invalid")
            card_number = self.data["card_number"]
            if not re.match(r"[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}", card_number):
                raise ValueError("card number is invalid")

    @property
    def serialized_data(self) -> dict:
        if self.instance is not None:
            card = {
                "id": self.instance.id,
                "bank_name": self.instance.bank.name,
                "card_number": self.instance.card_number,
                "cvv2": self.instance.cvv2,
                "expiration_date": self.instance.expiration_date,
            }
            return card
        else:
            return None
