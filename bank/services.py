from sqlalchemy.orm import Session

from bank.models import Bank, BankAccount
from source.database import DatabaseConnection
from users.models import User


def get_or_create_bank(name: str) -> Bank:
    with Session(DatabaseConnection.engin) as session:
        bank = session.query(Bank).filter_by(name=name).first()

        if bank is None:
            bank = Bank(name=name)
            session.add(bank)
            session.commit()

    return bank


def add_card(
    *,
    user: User,
    bank_name: str,
    card_number: str,
    cvv2: str,
    expiration_date: str,
    password: str
):
    bank = get_or_create_bank(name=bank_name)
    with Session(DatabaseConnection.engin) as session:
        card = BankAccount(
            card_number=card_number,
            cvv2=cvv2,
            expiration_date=expiration_date,
            password=password,
            user=user,
            bank=bank,
        )

        session.add(card)
        session.commit()


def deposit(card_id: int, amount: float):
    with Session(DatabaseConnection.engin) as session:
        account = (
            session.query(BankAccount).filter_by(id=card_id).with_for_update().one()
        )
        account.balance += amount
        session.commit()


def withdrawal(card_id: int, amount: float):
    session = Session()
    try:
        # Start a transaction
        account = (
            session.query(BankAccount).filter_by(id=card_id).with_for_update().one()
        )

        if account.balance >= amount:
            account.balance -= amount
        else:
            raise ValueError("insufficient funds")

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
