import sqlalchemy as db

from source.model import Base


class Bank(Base):
    __tablename__ = "banks"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
    )
    account = db.orm.relationship(
        "BankAccount",
        back_populates="bank",
    )


class BankAccount(Base):
    __tablename__ = "bank_accounts"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    card_number = db.Column(
        db.String(19),
        nullable=False,
        unique=True,
    )
    cvv2 = db.Column(
        db.String(255),
        nullable=False,
    )
    expiration_date = db.Column(
        db.String(5),
        nullable=False,
    )
    password = db.Column(
        db.String(255),
        nullable=False,
    )
    user_id = db.orm.mapped_column(
        db.ForeignKey("users.id"),
        nullable=False,
    )
    user = db.orm.relationship(
        "User",
        back_populates="bank_account",
    )
    bank_id = db.orm.mapped_column(
        db.ForeignKey("banks.id"),
        nullable=False,
    )
    bank = db.orm.relationship(
        "Bank",
        back_populates="account",
    )
