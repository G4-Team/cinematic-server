import datetime
import json

from webob import Request

from source.decorators import admin_requirement, allowed_methods, auth_requirement
from source.response import JsonResponse
from users import selectors, services
from users.serializers import UserSerializer
from users.utils import creat_jwt_token


@allowed_methods(["POST"])
def register_user_view(request: Request) -> JsonResponse:
    response = JsonResponse()
    data = json.loads(request.body)
    serializer = UserSerializer(data=data)
    try:
        serializer.validate()
        services.add_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            birthday=data["birthday"],
        )
        response.status_code = 201
        response_data = {
            "message": "SUCCESSFUL: user created successfuly",
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


@allowed_methods(["GET"])
def get_user_view(request: Request, id: str) -> JsonResponse:
    response = JsonResponse()
    try:
        user = selectors.get_user(id=int(id))
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
        response.status_code = 401

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
        if user.password != data["password"]:
            raise ValueError("invalid credentilas")
        print("user.id=", user.id)
        services.update_user_info(user, last_login=datetime.datetime.now())
        token = creat_jwt_token(user_id=user.id)

        response.status_code = 200
        response.set_cookie(name="jwt", value=token, httponly=True)
        response_data = {
            "message": "SUCCESSFUL: user logged in",
        }
        response.text = json.dumps(response_data)

    except KeyError as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: please send {str(e.args)}",
        }
        response.text = json.dumps(response_data)
    except ValueError as e:
        response_data = {
            "message": f"ERROR: {str(e)}",
        }
        response.text = json.dumps(response_data)

    except Exception as e:
        response_data = {
            "message": f"ERROR: {str(e)}",
        }
        response.text = json.dumps(response_data)

    return response


@allowed_methods(["GET"])
@auth_requirement
def is_auth_view(request: Request) -> JsonResponse:
    response = Response()
    response_data = {
        "message": "Hello my dear :)",
    }
    response.text = json.dumps(response_data)
    return response
