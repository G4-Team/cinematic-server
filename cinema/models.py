import sqlalchemy as db

from source.model import Base

class Cinema(Base):
    __tablename__ = 'cinemas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    seats = db.orm.relationship('Seat', back_populates='cinema')


class Seat(Base):
    __tablename__ = 'seats'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)
    is_reserved = db.Column(db.BOOLEAN, nullable=False, default=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinema.id'), nullable=False)
    cinema = db.orm.relationship('Cinema', back_populates='seats')
    # One-to-one relationship with User
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # user = db.orm.relationship(back_populates='seat')
