import json

from source import test


class TestBankAddeView(test.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.add_card_url = "/bank/card/add/"
        self.clinet = test.Cilent()

        self.valid_data = {
            "bank_name": "saman",
            "card_number": "5022-2910-7080-9321",
            "cvv2": "234",
            "expiration_date": "28-03",
            "password": "13214",
            "balance": "12312308231.23",
        }
        self.valid_user_date = {
            "username": "testkia",
            "email": "testkia@gmail.com",
            "phone": "09123211231",
            "password": "1235431231@#",
            "birthday": "1989-08-22",
            "confirm_password": "1235431231@#",
        }
        self.add_user = self.clinet.send_request(
            url="/users/register/",
            method="POST",
            data=json.dumps(self.valid_user_date),
            content_type="application/json",
        )

        self.login_user = self.clinet.send_request(
            url="/users/login/",
            method="POST",
            data=json.dumps({"username": "testkia", "password": "1235431231@#"}),
            content_type="application/json",
        )
        self.user_id = json.loads(self.login_user.text)["user_id"]

        self.add_card_url = f"/bank/card/add/{self.user_id}/"
        self.view_list_url = f"/bank/card/list/{self.user_id}/"

    def test_create_card_with_valid_data(self):
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="POST",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_data["message"], "SUCCESSFUL: card created successfully"
        )

    def test_do_not_Send_bankname(self):
        del self.valid_data["bank_name"]
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="POST",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: please send ('bank_name',)")

    def test_do_not_Send_cvv2(self):
        del self.valid_data["cvv2"]
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="POST",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: please send ('cvv2',)")

    def test_do_not_Send_expiration_date(self):
        del self.valid_data["expiration_date"]
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="POST",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["message"], "ERROR: please send ('expiration_date',)"
        )

    def test_do_not_Send_password(self):
        del self.valid_data["password"]

        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="POST",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: please send ('password',)")

    def test_check_cart_duplicate(self):
        self.valid_data["card_number"] = "5022-2910-7080-9322"
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="POST",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )

        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response_data["message"], "SUCCESSFUL: card created successfully"
        )
        # create dupplicat card
        self.valid_data["card_number"] = "5022-2910-7080-9322"
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="POST",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )

        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_data["message"],
            "ERROR: card number -> this card number already exists",
        )

    def test_check_expiration_date(self):
        self.valid_data["expiration_date"] = "100"
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="POST",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: expiration date is invalid")

    def test_check_card_number_correct_input(self):
        self.valid_data["card_number"] = "13123"
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="POST",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: card number is invalid")

    def test_check_justnumerical_card_number(self):
        self.valid_data["card_number"] = "2132-3132-fasd-1233"
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="POST",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data["message"], "ERROR: card number is invalid")

    def test_not_authenticate_user(self):
        json_data = json.dumps(self.valid_data)

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="GET",
            data=json_data,
            content_type="application/json",
        )
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response_data["message"],
            "ERROR: access denied! you are not authenticated",
        )

    def test_method_not_allowed(self):
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )

        response = self.clinet.send_request(
            url=self.add_card_url,
            method="GET",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )
        response_data = json.loads(response.text)
        # print(response_data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response_data["message"],
            "ERROR: method [GET] not allowed",
        )


class TestDepositView(test.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.add_card_url = "/bank/card/add/"
        self.clinet = test.Cilent()

        self.valid_data = {
            "bank_name": "saman",
            "card_number": "5022-2910-7080-9321",
            "cvv2": "234",
            "expiration_date": "28-03",
            "password": "13214",
            "balance": "12312308231.23",
        }
        self.valid_user_date = {
            "username": "testkia",
            "email": "testkia@gmail.com",
            "phone": "09123211231",
            "password": "1235431231@#",
            "birthday": "1989-08-22",
            "confirm_password": "1235431231@#",
        }
        self.add_user = self.clinet.send_request(
            url="/users/register/",
            method="POST",
            data=json.dumps(self.valid_user_date),
            content_type="application/json",
        )
        # jwt, value = (
        #     self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        # )
        self.login_user = self.clinet.send_request(
            url="/users/login/",
            method="POST",
            data=json.dumps({"username": "testkia", "password": "1235431231@#"}),
            content_type="application/json",
        )
        self.user_id = json.loads(self.login_user.text)["user_id"]

        self.add_card_url = f"/bank/card/add/{self.user_id}/"
        self.view_list_url = f"/bank/card/list/{self.user_id}/"

        self.aded_card = self.clinet.send_request(
            url=self.add_card_url,
            method="Post",
            data=json.dumps(self.valid_data),
            content_type="application/json",
        )

    def test_getidcard(self):
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )
        get_id_card = self.clinet.send_request(
            url=self.view_list_url,
            method="GET",
            data=json.dumps(self.valid_data),
            content_type="application/json",
            cookies={"jwt": value},
        )
        print(1)
        response_json = json.loads(get_id_card.text)
        print(json.dumps(response_json.get("cards", {}), indent=4))

        # response = json.loads(get_id_card.text)
        # self.card_id = response["cards"]["card1"]["id"]
        # print(self.card_id)

        # self.deposit_view_url = f"/bank/card/deposit/{self.user_id}/{self.card_id}/"

    # def test_check_card_is_invalid(self):
    #     self.valid_data["card_number"] = "5022-2910-7080-9322"
    #     jwt, value = (
    #         self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
    #     )
    #     response = self.clinet.send_request(
    #         url = self.deposit_view_url,
    #         method="POST",
    #         data=json.dumps(self.valid_data),
    #         content_type="application/json",
    #         cookies={"jwt": value},
    #     )
    #     print(response.text)
    #     print(response.status_code)
    #     response_data = json.loads(response.text)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(
    #         response_data["message"], "card invalid"
    #     )


class TestListCardView(test.TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.add_card_url = "/bank/card/add/"
        self.clinet = test.Cilent()

        self.valid_data = {
            "bank_name": "saman",
            "card_number": "5022-2910-7080-9321",
            "cvv2": "234",
            "expiration_date": "28-03",
            "password": "13214",
            "balance": "12312308231.23",
        }
        self.valid_user_date = {
            "username": "testkia",
            "email": "testkia@gmail.com",
            "phone": "09123211231",
            "password": "1235431231@#",
            "birthday": "1989-08-22",
            "confirm_password": "1235431231@#",
        }
        self.add_user = self.clinet.send_request(
            url="/users/register/",
            method="POST",
            data=json.dumps(self.valid_user_date),
            content_type="application/json",
        )

        self.login_user = self.clinet.send_request(
            url="/users/login/",
            method="POST",
            data=json.dumps({"username": "testkia", "password": "1235431231@#"}),
            content_type="application/json",
        )
        self.user_id = json.loads(self.login_user.text)["user_id"]

        self.add_card_url = f"/bank/card/add/{self.user_id}/"
        self.view_list_url = f"/bank/card/list/{self.user_id}/"

        self.aded_card = self.clinet.send_request(
            url=self.add_card_url,
            method="Post",
            data=json.dumps(self.valid_data),
            content_type="application/json",
        )

    def test_view_list_card(self):
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )
        response = self.clinet.send_request(
            url=self.view_list_url,
            method="GET",
            data=json.dumps({}),
            content_type="application/json",
            cookies={"jwt": value},
        )

        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response_data["message"], "SUCCESSFUL: cards retrived successfully"
        )

    def test_method_not_allowed(self):
        jwt, value = (
            self.login_user.headers.getall("Set-Cookie")[0].split(";")[0].split("=")
        )
        response = self.clinet.send_request(
            url=self.view_list_url,
            method="Post",
            data=json.dumps({}),
            content_type="application/json",
            cookies={"jwt": value},
        )

        response_data = json.loads(response.text)
        # print(response_data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response_data["message"],
            "ERROR: method [Post] not allowed",
        )
