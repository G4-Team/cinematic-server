import sqlalchemy

from settings.base import DATABASE_CONNECT_STR


class DatabaseConnection:
    engin = None

    @classmethod
    def create_engin(cls, db_url=None):
        db_url = db_url or DATABASE_CONNECT_STR
        cls.engin = sqlalchemy.create_engine(db_url)
        return cls.engin
