from webob import Request, Response
from parse import parse


class API:
    def __init__(self):
        self.routes  = dict()

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        
        return response(environ, start_response)

    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def response_404(self, response):
        response.status_code = 404
        response.text = 'Page not found'
    
    def find_handler(self, request_path):
        for path, handler in self.routes.items():
            if path == request_path:
                return handler, None

            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named

        return None, None

    def handle_request(self, request):
        user_agent = request.headers.get('User-Agent', 'None')
        
        path = request.path_info
        response = Response()

        handler, kwargs = self.find_handler(path)
        if handler is None:
            self.response_404(response)
        else:
            if kwargs:
                handler(request, response, **kwargs)
            else:
                handler(request, response)

        return response
        