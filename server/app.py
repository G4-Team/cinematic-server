from parse import parse
from webob import Request, Response


class Server:
    def __init__(self) -> None:
        self.urls = {}

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
