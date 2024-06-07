import json

from webob import Request, Response

from users import selectors, services
from users.serializers import UserSerializer


def add_user_view(request: Request) -> Response:
    response = Response()
    response.content_type = "application/json"

    data = request.params
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


def get_user_view(request: Request, id: str) -> Response:
    response = Response()
    response.content_type = "application/json"
    try:
        user = selectors.get_user(id=int(id))

        response.status_code = 200
        response_data = {
            "message": "SUCCESSFUL: user catch successfuly",
            "user": user_serializer(user=user),
        }
        response.text = json.dumps(response_data)

    except Exception as e:
        response.status_code = 401

        response_data = {
            "message": "ERROR: " + str(e),
        }
        response.text = json.dumps(response_data)

    return response
