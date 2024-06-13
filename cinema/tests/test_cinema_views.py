import json

from source import test
from users.services import create_admin


class TestAddCinemaView(test.TestCase):

    def setUp(self) -> None:
        super().setUp()

        self.url = "/cinema/add-cinema/"
        self.clinet = test.Cilent()
        self.valid_data = {
            "name": "pardis",
            "ticket_price": 100,
            "capacity": 30,
            "number_of_row": 6,
            "number_of_col": 5,
        }

        self.valid_admin_data = {
            "username": "admin",
            "email": "admin@email.com",
            "password": "123456789@#",
            "birthday": "2000-03-01",
        }
        create_admin(**self.valid_admin_data)

        self.login_admin = self.clinet.send_request(
            url="/users/login/",
            method="POST",
            data=json.dumps({"username": "admin", "password": "123456789@#"}),
            content_type="application/json",
        )

    def test_create_cinema_with_valid_data(self):
        jwt, value = (
            self.login_admin.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )
        response = self.clinet.send_request(
            url=self.url,
            data=json.dumps(self.valid_data),
            method="POST",
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_data["message"], "SUCCESSFUL: cinema created successfully"
        )
