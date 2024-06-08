import sqlalchemy as db

from source.model import Base


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
    )
    user_id = db.orm.mapped_column(db.ForeignKey("users.id"), nullable=True)
    user = db.orm.relationship("User", back_populates="wallet")
