from sqlalchemy import update
from sqlalchemy.orm import Session

from bank.models import Wallet
from source.database import DatabaseConnection
from users.models import User


def add_user(
    *, username: str, email: str, phone=None | str, password: str, birthday: str
) -> None:
    session = Session(DatabaseConnection.engin)
    user = User(
        username=username,
        email=email,
        password=password,
        birthday=birthday,
    )
    wallet = Wallet(
        balance=0,
        user=user,
    )
    session.add(user)
    session.add(wallet)
    session.commit()


def update_user_info(user: User, **kwargs):
    conn = DatabaseConnection.engin.connect()
    stmt = update(User).where(User.id == user.id).values(kwargs)
    conn.execute(stmt)
