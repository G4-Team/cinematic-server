import unittest

from sqlalchemy.orm import sessionmaker
from webob import Request, Response

from settings.base import BASE_DIR, URLS_DIR
from source import wsgi
from source.database import DatabaseConnection
from source.model import Base
from source.url import UrlManager


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = DatabaseConnection.create_engin(
            db_url=f"sqlite:///{BASE_DIR}/test.db"
        )
        Base.metadata.create_all(cls.engine)
        cls.connection = cls.engine.connect()
        cls.Session = sessionmaker(bind=cls.engine)

    # def tearDown(self):
    #     Base.metadata.drop_all(self.connection)

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
        cls.engine.dispose()


w = wsgi.WSGIHandler()
UrlManager(wsgi=w, directory_path=URLS_DIR).submit_urls()


class Cilent:
    def __init__(self) -> None:
        pass

    def send_request(self, *, url, method, data, content_type) -> Response:
        __request = Request.blank(path=url)
        __request.body = data.encode("utf-8")
        __request.method = method
        __request.content_type = content_type
        response = w.handle_request(request=__request)
        return response
