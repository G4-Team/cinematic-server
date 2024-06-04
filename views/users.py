from webob import Request, Response


def add_user(request: Request) -> Response:
    response = Response()

    response.status = 200
    response.text = "Add user"

    return response
