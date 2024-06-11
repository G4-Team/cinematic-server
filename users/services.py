from enum import Enum

from sqlalchemy import update
from sqlalchemy.orm import Session

from cinema.models import Subscription
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
            wallet=0,
        )
        s = Subscription(
            type_subscription="bronze",
            validity_duration=None,
            price=0,
            user=user,
            credit=0,
        )
        session.add(user)
        session.add(s)
        session.commit()


def update_user_info(user: User, **kwargs):
    stmt = update(User).where(User.id == user.id).values(kwargs)
    with DatabaseConnection.engin.begin() as conn:
        conn.execute(statement=stmt)


def buy_subscription(user_id: int, type_subscription: str):
    class TypeSubscription(Enum):
        bronze = 0
        silver = 3
        gold = 6

    session = Session(DatabaseConnection.engin)
    try:
        # Start a transaction

        user = session.query(User).filter_by(id=user_id).with_for_update().one()

        if user.wallet >= TypeSubscription[type_subscription].value * 100:
            user.wallet -= TypeSubscription[type_subscription].value * 100
            session.delete(user.subscription)
            s = Subscription(
                type_subscription=TypeSubscription[type_subscription].name,
                validity_duration=TypeSubscription[type_subscription].value,
                price=TypeSubscription[type_subscription].value * 100,
                user=user,
            )
            if TypeSubscription[type_subscription].value == 3:
                s.credit = 3
            elif TypeSubscription[type_subscription].value == 6:
                s.credit = 5
            else:
                s.credit = 0

        else:
            raise ValueError(
                f"insufficient funds. your balance: {user.wallet} - subscription price: {TypeSubscription[type_subscription].value * 100}"
            )

        session.add(s)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
