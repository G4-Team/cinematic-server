import sqlalchemy as db
from sqlalchemy.orm import Mapped
from source.model import Base


class Cinema(Base):
    __tablename__ = 'cinemas'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    ticket_price = db.Column(db.BigInteger, nullable=False)
    manager: Mapped['User'] = db.orm.relationship(back_populates='cinemas')
    show_times: Mapped['Showtime'] = db.orm.relationship(back_populates='cinema')
    capacity = db.Column(db.Integer, nullable=False)
    number_of_row = db.Column(db.Integer, nullable=False)
    number_of_col = db.Column(db.Integer, nullable=False)


class Showtime(Base):
    __tablename__ = 'showtimes'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    cinema_id = db.Column(db.Integer, db.ForeignKey('cinemas.id'), nullable=False)
    cinema: Mapped['Cinema'] = db.orm.relationship(back_populates='show_times')
    show_time = db.Column(db.DateTime, nullable=False)
    seats: Mapped['ShowtimeSeats'] = db.orm.relationship(back_populates='showtime')
    movie: Mapped['Movie'] = db.orm.relationship(back_populates='show_times')

class ShowtimeSeats(Base):
    __tablename__ = 'showtime_seats'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    showtime_id = db.Column(db.BigInteger, db.ForeignKey('showtimes.id'), nullable=False)
    showtime: Mapped['Showtime'] = db.orm.relationship(back_populates='seats')
    is_reserved = db.Column(db.Boolean, nullable=False, default=False)
    reserved_by: Mapped['User'] = db.orm.relationship(back_populates='reservations')
    row = db.Column(db.Integer, nullable=False)
    col = db.Column(db.Integer, nullable=False)
