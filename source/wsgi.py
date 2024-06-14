import json

from parse import parse
from webob import Request, Response

from settings.base import BASE_DIR
from source.response import JsonResponse


class WSGIHandler:
    def __init__(self) -> None:
        self.urls = {
            "/": self.response_home,
        }

    def __call__(self, environ, start_response):
        request = Request(environ=environ)

        response = self.handle_request(request=request)

        return response(environ=environ, start_response=start_response)

    def find_handler(self, request_path):
        for path, handler in self.urls.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        path = request.path
        handler, kwargs = self.find_handler(request_path=path)
        if handler is not None:
            response = handler(request, **kwargs)
        else:
            response = self.response_404()

        return response

    def response_404(self):
        response = Response()
        response.status_code = 404
        response.text = "Not found!"

        return response

    def response_home(self, request):
        response = Response()
        response.content_type = "text/html"
        models_filename = BASE_DIR / "document" / "urls-document.html"
        with open(models_filename, "r") as f:
            html_help_content = f.read()

        response.text = html_help_content
        return response

    def response_access_denied_not_auth(request):
        response = JsonResponse()
        response.status_code = 401
        response_data = {
            "message": "ERROR: access denied! you are not authenticated",
        }
        response.text = json.dumps(response_data)

        return response

    def response_access_denied_not_owner(request):
        response = JsonResponse()
        response.status_code = 403
        response_data = {
            "message": "ERROR: access denied! you are not owner",
        }
        response.text = json.dumps(response_data)

        return response

    def response_access_denied_not_admin(request):
        response = JsonResponse()
        response.status_code = 403
        response_data = {
            "message": "ERROR: access denied! only admin access this url",
        }
        response.text = json.dumps(response_data)

        return response

    def response_method_not_allowed(request):
        response = JsonResponse()
        response.status_code = 405
        response_data = {
            "message": f"ERROR: method [{request.method}] not allowed",
        }
        response.text = json.dumps(response_data)

        return response
