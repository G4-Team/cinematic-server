import json

from webob import Request

from bank import selectors, services
from source.decorators import allowed_methods, auth_requirement, owner_requirement
from source.response import JsonResponse
from users.selectors import get_user


@owner_requirement
@auth_requirement
@allowed_methods(["POST"])
def add_card_view(request: Request, user_id):
    response = JsonResponse()

    data = json.loads(request.body)

    try:
        user = get_user(id=int(user_id))
        services.add_card(
            user=user,
            bank_name=data["bank_name"],
            cvv2=data["cvv2"],
            password=data["password"],
        )

        response.status_code = 201
        response_data = {
            "message": "SUCCESSFUL: card created successfully",
        }
        response.text = json.dumps(response_data)
    except KeyError as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: please send {str(e.args)}",
        }
        response.text = json.dumps(response_data)

    return response
