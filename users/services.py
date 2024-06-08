from sqlalchemy import update
from sqlalchemy.orm import Session

from bank.models import Wallet
from source.database import DatabaseConnection
from users.models import User


def add_user(
    *, username: str, email: str, phone: None | str = None, password: str, birthday: str
) -> None:
    with Session(DatabaseConnection.engin) as session:
        user = User(
            username=username,
            email=email,
            phone=phone,
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
    stmt = update(User).where(User.id == user.id).values(kwargs)
    with DatabaseConnection.engin.begin() as conn:
        conn.execute(statement=stmt)
