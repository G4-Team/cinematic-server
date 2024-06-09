import json

from webob import Request

from bank import selectors, services
from bank.serializers import CardSerializer
from source.decorators import allowed_methods, auth_requirement, owner_requirement
from source.response import JsonResponse
from users.selectors import get_user


@owner_requirement
@auth_requirement
@allowed_methods(["POST"])
def add_card_view(request: Request, user_id):
    response = JsonResponse()

    data = json.loads(request.body)
    serializer = CardSerializer(data=data)
    try:
        user = get_user(id=int(user_id))
        serializer.validate()
        services.add_card(
            user=user,
            bank_name=data["bank_name"],
            card_number=data["card_number"],
            cvv2=data["cvv2"],
            expiration_date=data["expiration_date"],
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


@owner_requirement
@auth_requirement
@allowed_methods(["GET"])
def list_cards_view(request: Request, user_id):
    response = JsonResponse()

    try:
        cards = selectors.get_cards(user_id=int(user_id))
        response_data = {
            "message": "SUCCESSFUL: cards retrived successfully",
            "cards": {},
        }
        for index, card in enumerate(cards):
            response_data["cards"][f"card{index}"] = CardSerializer(
                instance=card
            ).serialized_data
        response.status_code = 200

        response.text = json.dumps(response_data)
    except Exception as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: {str(e.args)}",
        }
        response.text = json.dumps(response_data)

    return response
