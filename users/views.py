import datetime
import json

from webob import Request

from bank.selectors import filter_cards
from bank.services import charge_wallet
from source.decorators import (allowed_methods, auth_requirement,
                               owner_requirement)
from source.response import JsonResponse
from users import selectors, services
from users.serializers import UserSerializer
from users.utils import creat_jwt_token, hash_password


@allowed_methods(["POST"])
def register_user_view(request: Request) -> JsonResponse:
    response = JsonResponse()
    data = json.loads(request.body)
    serializer = UserSerializer(data=data)
    # try:
    serializer.validate()
    services.add_user(
        username=data["username"],
        email=data["email"],
        phone=data.get("phone", None),
        password=hash_password(data["password"]),
        birthday=data["birthday"],
    )
    response.status_code = 201
    response_data = {
        "message": "SUCCESSFUL: user created successfuly",
    }
    response.text = json.dumps(response_data)
    # except KeyError as e:
    #     response.status_code = 400
    #     response_data = {
    #         "message": f"ERROR: please send {str(e.args)}",
    #     }
    #     response.text = json.dumps(response_data)
    # except Exception as e:
    #     response.status_code = 400
    #     response_data = {
    #         "message": f"ERROR: {str(e)}",
    #     }
    #     response.text = json.dumps(response_data)

    return response


@owner_requirement
@auth_requirement
@allowed_methods(["GET"])
def profile_view(request: Request, user_id: str) -> JsonResponse:
    response = JsonResponse()
    try:
        user = selectors.get_user(id=int(user_id))
        if user is None:
            response.status = 404
            response_data = {
                "message": "ERROR: user not foud!",
            }
            response.text = json.dumps(response_data)
            return response

        serializer = UserSerializer(instance=user)
        response.status_code = 200
        response_data = {
            "message": "SUCCESSFUL: user catch successfuly",
            "user": serializer.serialized_data,
        }
        response.text = json.dumps(response_data)

    except Exception as e:
        response.status_code = 400

        response_data = {
            "message": "ERROR: " + str(e),
        }
        response.text = json.dumps(response_data)

    return response


@allowed_methods(["POST"])
def login_view(request: Request) -> JsonResponse:
    response = JsonResponse()
    data = json.loads(request.body)
    try:
        user = selectors.filter_users(username=data["username"]).first()
        if user is None:
            raise ValueError("invalid credentilas")
        if user.password != hash_password(data["password"]):
            raise ValueError("invalid credentilas")
        services.update_user_info(user, last_login=datetime.datetime.now())
        token = creat_jwt_token(user_id=user.id)

        response.status_code = 200
        response.set_cookie(name="jwt", value=token, httponly=True)
        response_data = {
            "message": "SUCCESSFUL: user logged in",
            "user_id": user.id,
            "is_admin": user.is_admin,
        }
        response.text = json.dumps(response_data)

    except KeyError as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: please send {str(e.args)}",
        }
        response.text = json.dumps(response_data)
    except ValueError as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: {str(e)}",
        }
        response.text = json.dumps(response_data)

    except Exception as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: {str(e)}",
        }
        response.text = json.dumps(response_data)

    return response


@owner_requirement
@auth_requirement
@allowed_methods(["PUT"])
def change_profile_view(request: Request, user_id):
    response = JsonResponse()
    data = json.loads(request.body)
    allowed_data = {}
    if "username" in data:
        allowed_data["username"] = data["username"]
    if "email" in data:
        allowed_data["email"] = data["email"]
    if "phone" in data:
        allowed_data["phone"] = data["phone"]
    if "birthday" in data:
        allowed_data["birthday"] = data["birthday"]

    serializer = UserSerializer(data=allowed_data, partial=True)
    try:
        serializer.validate()
        user = selectors.get_user(id=int(user_id))
        services.update_user_info(user, **allowed_data)
        response.status_code = 200
        response_data = {
            "message": "SUCCESSFUL: user updated successfully",
        }
        response.text = json.dumps(response_data)
    except Exception as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: {str(e)}",
        }
        response.text = json.dumps(response_data)

    return response


@owner_requirement
@auth_requirement
@allowed_methods(["PUT"])
def change_password_view(request: Request, user_id):
    response = JsonResponse()
    data = json.loads(request.body)
    allowed_data = {}
    try:
        allowed_data["password"] = data["password"]
        serlializer = UserSerializer(data=allowed_data, partial=True)
        serlializer.validate()

        user = selectors.get_user(id=int(user_id))

        if user.password != hash_password(data["old_password"]):
            raise ValueError("incorrect old password")
        if data["password"] != data["confirm_password"]:
            raise ValueError("new password and confirm new password doesn't match")

        allowed_data["password"] = hash_password(allowed_data["password"])
        services.update_user_info(user, **allowed_data)
        response.status_code = 200
        response_data = {
            "message": "SUCCESSFUL: password updated successfully",
        }
        response.text = json.dumps(response_data)
    except KeyError as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: please send {str(e.args)}",
        }
        response.text = json.dumps(response_data)
    except Exception as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: {str(e)}",
        }
        response.text = json.dumps(response_data)

    return response


@owner_requirement
@auth_requirement
@allowed_methods(["PUT"])
def charge_wallet_view(request: Request, user_id):
    response = JsonResponse()

    f = open("./logs/transaction.log", "a")
    f.write(
        f"\n\n----- new *withdrawal - charge wallet* transaction ----- {datetime.datetime.now()}\n\n"
    )
    f.write(f"url: {request.path}\n")
    f.write(f"user_id: {user_id}\n")

    try:
        data = json.loads(request.body)
        f.write(f"data: {data}\n")
        card = filter_cards(
            card_number=data["card_number"],
            cvv2=data["cvv2"],
            expiration_date=data["expiration_date"],
            password=hash_password(data["password"]),
        ).first()

        if card is None:
            raise ValueError("card invalid")

        if int(user_id) != card.user_id:
            raise PermissionError("you are not owner of this card")

        charge_wallet(int(user_id), int(card.id), amount=data["amount"])

        response.status_code = 200
        response_data = {
            "message": "SUCCESSFUL: transaction successful",
        }

    except KeyError as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: please send {str(e.args)}",
        }
    except PermissionError as e:
        response.status_code = 403
        response_data = {
            "message": f"ERROR: {str(e)}",
        }
    except Exception as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: {str(e)}",
        }

    f.write(f"-> response status code: {response.status_code}\n")
    f.write(f'-> response content: {response_data["message"]}\n')
    f.write(f"\n----- end of transaction ----- {datetime.datetime.now()}\n\n")
    f.close()

    response.text = json.dumps(response_data)
    return response


@owner_requirement
@auth_requirement
@allowed_methods(["PUT"])
def buy_subscription_view(request: Request, user_id):
    response = JsonResponse()
    try:
        data = json.loads(request.body)
        services.buy_subscription(
            int(user_id), type_subscription=data["type_subscription"]
        )
        response.status_code = 200
        response_data = {
            "message": "SUCCESSFUL: transaction successful",
        }
    except KeyError:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: please send a valid subscription",
        }
    except Exception as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: {str(e)}",
        }

    response.text = json.dumps(response_data)
    return response
