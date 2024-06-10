import json

from webob import Request

from movie import selectors, services
from movie.serializers import MovieSerializer
from source.decorators import admin_requirement, allowed_methods, auth_requirement
from source.response import JsonResponse


@admin_requirement
@allowed_methods(["POST"])
def add_movie_view(request: Request) -> JsonResponse:
    response = JsonResponse()

    data = json.loads(request.body)

    serializer = MovieSerializer(data=data)

    try:
        serializer.validate()
        services.add_movie(name=data["name"])

        response.status_code = 201
        response_data = {
            "message": "SUCCESSFUL: movie created successfully",
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


@auth_requirement
@allowed_methods(["POST"])
def add_movie_review_view(request: Request, user_id, movie_id) -> JsonResponse:
    response = JsonResponse()
    data = json.loads(request.body)

    try:
        services.add_movie_review(
            rate=data["rate"],
            text=data["text"],
            user_id=int(user_id),
            movie_id=int(movie_id),
        )
        response.status_code = 201
        response_data = {
            "message": "SUCCESSFUL: review was submitted successfully",
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


@auth_requirement
@allowed_methods(["POST"])
def add_comment_movie_review_view(request: Request, user_id, review_id) -> JsonResponse:
    response = JsonResponse()

    data = json.loads(request.body)

    try:
        services.add_comment_movie_review(
            text=data["text"],
            user_id=int(user_id),
            review_id=int(review_id),
        )
        response.status_code = 201
        response_data = {
            "message": "SUCCESSFUL: comment was submitted successfully",
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


@allowed_methods(["GET"])
def list_movie_comments_view(request: Request, movie_id) -> JsonResponse:
    response = JsonResponse()
    try:
        response.status_code = 200
        response_data = {
            "message": "SUCCESSFUL: movie comments retrived successfully",
            "movie_comments": selectors.list_commets(int(movie_id)),
        }

    except Exception as e:
        response.status_code = 400
        response_data = {
            "message": f"ERROR: {str(e)}",
        }

    response.text = json.dumps(response_data)

    return response

