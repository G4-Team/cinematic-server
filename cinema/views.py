import json

from webob import Request

from cinema import selectors, services
from cinema.serializers import (
    CinemaSerializer,
    ShowtimeSeatSerializer,
    ShowtimeSerializer,
)
from source.decorators import (
    admin_requirement,
    allowed_methods,
    auth_requirement,
    owner_requirement,
)
from source.response import JsonResponse
from users.selectors import get_user


@admin_requirement
@auth_requirement
@allowed_methods(["POST"])
def add_cinema_view(request: Request) -> JsonResponse:
    response = JsonResponse()
    data = json.loads(request.body)
    serializer = CinemaSerializer(data=data)
    try:
        serializer.validate()
        services.add_cinema(
            name=data["name"],
            ticket_price=data["ticket_price"],
            capacity=data["capacity"],
            number_of_row=data["number_of_row"],
            number_of_col=data["number_of_col"],
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


@admin_requirement
@auth_requirement
@allowed_methods(["POST"])
def add_showtime_view(request: Request) -> JsonResponse:
    response = JsonResponse()
    data = json.loads(request.body)
    serializer = ShowtimeSerializer(data=data)
    try:
        cinema = selectors.filter_cinemas(name=data["cinema_name"]).first()
        if cinema is None:
            raise ValueError("cinema doesn't exist")

        serializer.validate()

        services.add_showtime(
            time=data["time"],
            cinema_id=cinema.id,
            movie_name=data["movie_name"],
            movie_age_rating=int(data["movie_age_rating"]),
        )
        response.status_code = 201
        response_data = {
            "message": "SUCCESSFUL: showtime created successfully",
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
@allowed_methods(["GET"])
def list_showtimes_view(request: Request, user_id: int) -> JsonResponse:
    response = JsonResponse()

    try:
        user = get_user(int(user_id))
        showtimes = selectors.get_showtimes(user=user)
        response_data = {
            "message": "SUCCESSFUL: showtimes retrived successfully",
            "showtimes": {},
        }
        for index, showtime in enumerate(showtimes):
            response_data["showtimes"][f"showtime{index}"] = ShowtimeSerializer(
                instance=showtime
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


@auth_requirement
@allowed_methods(["GET"])
def list_showtime_seats(request: Request, showtime_id) -> JsonResponse:
    response = JsonResponse()

    try:
        seats = selectors.get_showtime_seats(showtime_id=int(showtime_id))
        response_data = {
            "message": "SUCCESSFUL: seats retrived successfully",
            "seats": {},
        }
        for index, seat in enumerate(seats):
            response_data["seats"][index] = ShowtimeSeatSerializer(
                instance=seat[0]
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
def reserve_showtime_view(request: Request, user_id, showtime_seat_id) -> JsonResponse:
    response = JsonResponse()

    try:
        services.reserve_seat(user_id=int(user_id), seat_id=int(showtime_seat_id))
        response.status_code = 200
        response_data = {
            "message": "SUCCESSFUL: showtime seat reserved successfully",
        }
    except Exception as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: {str(e)}",
        }

    response.text = json.dumps(response_data)
    return response
