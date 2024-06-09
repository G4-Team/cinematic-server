import datetime
import json

from webob import Request, Response

from cinema import selectors, services
from source.decorators import allowed_methods, auth_requirement, owner_requirement
from source.response import JsonResponse
from cinema.serializers import CinemaSerializer

@allowed_methods(["POST"])
def add_cinema_view(request: Request) -> JsonResponse:
    response = JsonResponse()
    data = json.loads(request.body)
    serializer = CinemaSerializer(data=data)
    try:
        serializer.validate()
        services.add_cinema(
            name=data['name'],
            ticket_price=data['ticket_price'],
            capacity=data['capacity'],
            number_of_row=data['number_of_row'],
            number_of_col=data['number_of_col'],
        )
        response.status_code = 201
        response_data = {
            "message": "SUCCESSFUL: cinema created successfully",
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