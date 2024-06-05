import sqlalchemy

from settings.base import DATABASE_CONNECT_STR


class DatabaseConnection:
    engin = None

    @classmethod
    def create_engin(cls):
        cls.engin = sqlalchemy.create_engine(DATABASE_CONNECT_STR)
