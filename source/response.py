from webob import Response


class JsonResponse(Response):
    def __init__(self, **kwargs):
        kwargs["content_type"] = "application/json"
        super().__init__(**kwargs)
