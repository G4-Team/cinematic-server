import json

from source import test
from users.services import create_admin


class TestAddMovieView(test.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.url = "/movie/add/"
        self.clinet = test.Cilent()

        self.valid_data = {
            "name": "Inglourious Basterds",
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

    def test_add_movie_with_valid_data(self):
        json_data = json.dumps(self.valid_data)
        jwt, value = (
            self.login_admin.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_data["message"], "SUCCESSFUL: movie created successfully"
        )

    def test_do_not_send_name(self):
        del self.valid_data["name"]
        json_data = json.dumps(self.valid_data)
        jwt, value = (
            self.login_admin.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )
        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: please send ('name',)")

    def test_duplicate_name_validation(self):
        json_data = json.dumps(self.valid_data)
        jwt, value = (
            self.login_admin.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
            cookies={"jwt": value},
        )
        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: this film already exists")

    def test_method_not_allowed(self):
        json_data = json.dumps(self.valid_data)
        jwt, value = (
            self.login_admin.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )
        response = self.clinet.send_request(
            url=self.url,
            method="GET",
            data=json_data,
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response_data["message"],
            "ERROR: method [GET] not allowed",
        )


class TestAddReviewView(test.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.url = "/movie/review/add/"
        self.clinet = test.Cilent()

        self.valid_data = {
            "rate": 4.5,
            "text": "TEST REVIEW",
        }

        self.valid_movie_data = {
            "name": "Inglourious Basterds",
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
        self.jwt, self.value = (
            self.login_admin.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )
        self.movie_request = self.clinet.send_request(
            url="/movie/add/",
            method="POST",
            data=json.dumps(self.valid_movie_data),
            content_type="application/json",
            cookies={"jwt": self.value},
        )

    def test_create_review_with_valid_data(self):
        movie_id = json.loads(self.movie_request.text)["movie"]["id"]
        user_id = json.loads(self.login_admin.text)["user_id"]

        self.url += f"{user_id}/{movie_id}/"

        json_data = json.dumps(self.valid_data)
        jwt, value = (
            self.login_admin.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_data["message"], "SUCCESSFUL: review was submitted successfully"
        )
        del response_data["review"]["created_at"]
        self.assertEqual(
            response_data["review"],
            {
                "id": 1,
                "text": "TEST REVIEW",
                "user_id": 1,
                "movie_id": 1,
                "rate": 4.5,
            },
        )

    def do_not_send_rate(self):
        movie_id = json.loads(self.movie_request.text)["movie"]["id"]
        user_id = json.loads(self.login_admin.text)["user_id"]

        self.url += f"{user_id}/{movie_id}/"

        del self.valid_data["rate"]
        json_data = json.dumps(self.valid_data)
        jwt, value = (
            self.login_admin.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "SUCCESSFUL: ")
