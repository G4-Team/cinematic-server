import unittest

from sqlalchemy.orm import sessionmaker
from webob import Request, Response

from settings.base import BASE_DIR, URLS_DIR
from source import wsgi
from source.database import DatabaseConnection
from source.model import Base
from source.url import UrlManager


class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = DatabaseConnection.create_engin(
            db_url=f"sqlite:///{BASE_DIR}/test.db"
        )
        Base.metadata.create_all(self.engine)
        self.connection = self.engine.connect()
        self.Session = sessionmaker(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.connection)
        self.connection.close()
        self.engine.dispose()


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
