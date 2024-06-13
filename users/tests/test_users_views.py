import json

from source import test


class TestUserRegisterView(test.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.url = "/users/register/"
        self.clinet = test.Cilent()

        self.valid_data = {
            "username": "test",  # only alphabet and numbers - less than 100 char
            "email": "test3@email.com",  # valid email format
            "phone": "09135556622",  # (optoinal) valif phone number format
            "password": "123456789@#",  # at least 8 char - contain at least two characters from #$@&
            "confirm_password": "123456789@#",
            "birthday": "2000-03-01",  # valid birthday format yyyy-mm-dd
        }

    def test_create_user_with_valid_data(self):
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_data["message"], "SUCCESSFUL: user created successfuly"
        )

    def test_do_not_send_username(self):
        del self.valid_data["username"]
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: please send ('username',)")

    def test_do_not_send_email(self):
        del self.valid_data["email"]
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: please send ('email',)")

    def test_do_not_send_phone(self):
        del self.valid_data["phone"]
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertNotEqual(response.status_code, 400)
        self.assertNotEqual(response_data["message"], "ERROR: please send ('phone',)")

    def test_do_not_send_password(self):
        del self.valid_data["password"]
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: please send ('password',)")

    def test_do_not_send_confirm_password(self):
        del self.valid_data["confirm_password"]
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["message"], "ERROR: please send ('confirm_password',)"
        )

    def test_do_not_send_birthday(self):
        del self.valid_data["birthday"]
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: please send ('birthday',)")

    def test_duplicate_username_validations(self):
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_data["message"], "SUCCESSFUL: user created successfuly"
        )

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["message"], "ERROR: username -> this username already exists"
        )

    def test_100char_username_validations(self):
        self.valid_data["username"] = "a" * 101
        json_data = json.dumps(self.valid_data)
        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["message"],
            "ERROR: username -> username must be less than 100 char",
        )

    def test_duplicate_email_validations(self):
        self.valid_data["username"] = "test1"
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_data["message"], "SUCCESSFUL: user created successfuly"
        )

        self.valid_data["username"] = "test2"
        json_data = json.dumps(self.valid_data)
        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["message"], "ERROR: email -> this email already exists"
        )

    def test_invalid_format_email_validation(self):
        self.valid_data["email"] = "123"
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: email -> email not valid")

    def test_invalid_format_phone_validation(self):
        self.valid_data["phone"] = "8" * 11
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: phone -> phone not valid")

    def test_at_least_8char_password_validatios(self):
        self.valid_data["password"] = "1"
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["message"],
            "ERROR: password -> password must contain at least 8 char",
        )

    def test_at_least_2special_char_password_validation(self):
        self.valid_data["password"] = "123456789"
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(
            response_data["message"],
            "ERROR: password -> password must contain at least two characters from #$@&",
        )

    def test_just_alphanumeric_and_special_char_password_validation(self):
        self.valid_data["password"] = "123456789@#."
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["message"],
            "ERROR: password -> password contains invalid characters. Only letters, numbers, and @#$& are allowed",
        )

    def test_confirm_password_validation(self):
        self.valid_data["password"] = "123456789@#"
        self.valid_data["confirm_password"] = "1234567@#"
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        # print(response_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["message"],
            "ERROR: canforim password -> password and it's confirm doesn't match",
        )

    def test_valid_format_birthday_validation(self):
        self.valid_data["birthday"] = "200"
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="POST",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        # print(response_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["message"],
            "ERROR: birthday -> birthday is invalid",
        )

    def test_method_not_allowed(self):
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.url,
            method="GET",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        # print(response_data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response_data["message"],
            "ERROR: method [GET] not allowed",
        )
