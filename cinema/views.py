import datetime
import json

from webob import Request, Response

from cinema import selectors, services
from source.decorators import allowed_methods, auth_requirement, admin_requirement
from source.response import JsonResponse
from cinema.serializers import CinemaSerializer, ShowtimeSerializer


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


@admin_requirement
@auth_requirement
@allowed_methods(["POST"])
def add_showtime_view(request: Request) -> JsonResponse:
    response = JsonResponse()
    data = json.loads(request.body)
    serializer = ShowtimeSerializer(data=data)
    try:
        serializer.validate()
        services.add_showtime(
            show_time=data['show_time'],
            cinema_id=data['cinema_id'],
            movie_id=data['movie_id'],
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


@auth_requirement
@allowed_methods(["GET"])
def list_showtimes_view(request: Request) -> JsonResponse:
    response = JsonResponse()

    try:
        showtimes = selectors.get_showtimes()
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
@allowed_methods(["POST"])
def list_movie_showtimes_view(request: Request, movie_id) -> JsonResponse:
    response = JsonResponse()

    try:
        showtimes = selectors.get_movie_showtimes(movie_id=int(movie_id))
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
@allowed_methods(["POST"])
def list_cinema_showtimes_view(request: Request, cinema_id) -> JsonResponse:
    response = JsonResponse()

    try:
        showtimes = selectors.get_cinema_showtimes(cinema_id=int(cinema_id))
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
@allowed_methods(["POST"])
def list_showtime_seats(request: Request, showtime_id) -> JsonResponse:
    response = JsonResponse()

    try:
        seats = selectors.get_showtime_seats(showtime_id=int(showtime_id))
        response_data = {
            "message": "SUCCESSFUL: seats retrived successfully",
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