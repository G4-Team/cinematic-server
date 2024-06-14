import json
from datetime import datetime

from webob import Request

from bank import selectors, services
from bank.serializers import CardSerializer
from source.decorators import (
    allowed_methods,
    auth_requirement,
    owner_requirement,
    tracker,
)
from source.response import JsonResponse
from users.selectors import get_user
from users.utils import hash_password


@tracker
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
            password=hash_password(data["password"]),
            balance=data["balance"],
        )

        response.status_code = 201
        response_data = {
            "message": "SUCCESSFUL: card created successfully",
        }

    except KeyError as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: please send {str(e.args)}",
        }

    except Exception as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: {str(e)}",
        }

    response.text = json.dumps(response_data)

    return response


@tracker
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


@owner_requirement
@auth_requirement
@allowed_methods(["POST"])
def deposit_view(request: Request, user_id, card_id):
    response = JsonResponse()

    f = open("./logs/transaction.log", "a")
    f.write(f"\n\n----- new *deposit* transaction ----- {datetime.now()}\n\n")
    f.write(f"url: {request.path}\n")
    f.write(f"user_id: {user_id} - card_id: {card_id}\n")

    try:
        data = json.loads(request.body)
        f.write(f"data: {data}\n")
        card = selectors.filter_cards(
            card_number=data["card_number"],
            cvv2=data["cvv2"],
            expiration_date=data["expiration_date"],
            password=hash_password(data["password"]),
        ).first()

        if card is None:
            raise ValueError("card invalid")

        if int(user_id) != card.user_id:
            raise PermissionError("you are not owner of this card")

        services.deposit(int(card_id), amount=data["amount"])

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
    f.write(f"\n----- end of transaction ----- {datetime.now()}\n\n")
    f.close()

    response.text = json.dumps(response_data)
    return response


@owner_requirement
@auth_requirement
@allowed_methods(["POST"])
def withdrawal_view(request: Request, user_id, card_id):
    response = JsonResponse()

    f = open("./logs/transaction.log", "a")
    f.write(f"\n\n----- new *withdrawal* transaction ----- {datetime.now()}\n\n")
    f.write(f"url: {request.path}\n")
    f.write(f"user_id: {user_id} - card_id: {card_id}\n")

    try:
        data = json.loads(request.body)
        f.write(f"data: {data}\n")
        card = selectors.filter_cards(
            card_number=data["card_number"],
            cvv2=data["cvv2"],
            expiration_date=data["expiration_date"],
            password=hash_password(data["password"]),
        ).first()

        if card is None:
            raise ValueError("card invalid")

        if int(user_id) != card.user_id:
            raise PermissionError("you are not owner of this card")

        services.withdrawal(int(card_id), amount=data["amount"])

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
    f.write(f"\n----- end of transaction ----- {datetime.now()}\n\n")
    f.close()

    response.text = json.dumps(response_data)
    return response


@owner_requirement
@auth_requirement
@allowed_methods(["POST"])
def wire_transfer_view(request: Request, user_id, sending_card_id):
    response = JsonResponse()

    f = open("./logs/transaction.log", "a")
    f.write(f"\n\n----- new *wire transfer* transaction ----- {datetime.now()}\n\n")
    f.write(f"url: {request.path}\n")
    f.write(f"user_id: {user_id} - card_id: {sending_card_id}\n")

    try:
        data = json.loads(request.body)
        f.write(f"data: {data}\n")
        sending_card = selectors.filter_cards(
            card_number=data["sending_card_number"],
            cvv2=data["cvv2"],
            expiration_date=data["expiration_date"],
            password=hash_password(data["password"]),
        ).first()

        if sending_card is None:
            raise ValueError("card invalid")

        if int(user_id) != sending_card.user_id:
            raise PermissionError("you are not owner of this card")

        receiving_card = selectors.filter_cards(
            card_number=data["receiving_card_number"],
        ).first()

        if receiving_card is None:
            raise ValueError("card invalid")

        services.wire_transfer(
            int(sending_card_id), receiving_card.id, amount=data["amount"]
        )

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
    f.write(f"\n----- end of transaction ----- {datetime.now()}\n\n")
    f.close()

    response.text = json.dumps(response_data)
    return response
