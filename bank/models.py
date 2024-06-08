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
    balance = db.Column(
        db.Float,
        default=0,
        nullable=False,
    )
    cvv2 = db.Column(
        db.String(255),
        nullable=False,
    )
    password = db.Column(
        db.String(255),
        nullable=False,
    )
    user_id = db.orm.mapped_column(db.ForeignKey("users.id"), nullable=True)
    user = db.orm.relationship("User", back_populates="bank_account")
    bank_id = db.orm.mapped_column(db.ForeignKey("banks.id"), nullable=True)
    bank = db.orm.relationship("Bank", back_populates="account")


class Wallet(Base):
    __tablename__ = "wallets"
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    balance = db.Column(
        db.Float,
        default=0,
        nullable=False,
    )
    user_id = db.orm.mapped_column(db.ForeignKey("users.id"), nullable=True)
    user = db.orm.relationship("User", back_populates="wallet")
