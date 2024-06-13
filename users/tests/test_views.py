import http.client
import json

from source import test


class TestUserRegisterView(test.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.host = "127.0.0.1"
        self.port = 8000
        self.header = {"Content-type": "application/json"}
        self.conn = http.client.HTTPConnection(self.host, self.port)

        self.clinet = test.Cilent()

        self.valid_data = {
            "username": "test3",  # only alphabet and numbers - less than 100 char
            "email": "test3@email.com",  # valid email format
            "phone": "09135556622",  # (optoinal) valif phone number format
            "password": "123456789@#",  # at least 8 char - contain at least two characters from #$@&
            "confirm_password": "123456789@#",
            "birthday": "2000-03-01",  # valid birthday format yyyy-mm-dd
        }

    def test_do_not_send_required_data(self):

        url = "/users/register/"

        # username
        # data = {
        #     "username": "x",
        # }
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        print(response_data)
        # self.assertEqual(response.status, 201)
        # self.assertEqual(response_data["username"], "testuser2")

        # email
