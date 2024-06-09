from bank.models import Bank, BankAccount
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
            pass
        pass

    @property
    def serialized_data(self) -> dict:
        if self.instance is not None:
            card = {
                "id": self.instance.id,
                "bank_name": self.instance.bank.name,
                "cvv2": self.instance.cvv2,
                "balance": self.instance.balance,
            }
            return card
        else:
            return None
