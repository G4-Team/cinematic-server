import json

from webob import Request

from movie import selectors, services
from movie.serializers import MovieSerializer
from source.decorators import admin_requirement, allowed_methods
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
