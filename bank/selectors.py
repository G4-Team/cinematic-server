from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.orm.query import Query

from bank.models import Bank, BankAccount
from source.database import DatabaseConnection


def get_cards(user_id: int) -> Query:
    stmt = (
        select(BankAccount, Bank)
        .options(selectinload(BankAccount.bank))
        .where(BankAccount.user_id == user_id)
        .join(Bank)
    )
    result = []
    with Session(DatabaseConnection.engin) as session:
        for row in session.execute(stmt):
            result.append(row[0])
    return result


def get_card(card_id: int) -> BankAccount:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(BankAccount)
        card = query.get(id)
    return card


def filter_cards(**kwargs) -> Query:
    with Session(DatabaseConnection.engin) as session:
        query = session.query(BankAccount)
        cards = query.filter_by(**kwargs)
    return cards
