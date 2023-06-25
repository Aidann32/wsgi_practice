from wsgiref.simple_server import make_server


class Routeware:
    def __init__(self, app, routes):
        self.wrapped_app = app
        self.routes = routes

    def __call__(self, environ, start_response, *args, **kwargs):
        wrapped_app_response = self.wrapped_app(environ, start_response) 
        return [data[::-1] for data in wrapped_app_response]

# Мы получаем тело запроса и всю остальную информацию в environ
# start_response функция, которая отвечает клиенту на его запрос
# В application встраивается функция start_response(со стороны фреймворка которая отвечает как отвечать запрос)
def application(environ, start_response):
    response = [
        f'{key}: {value}' for key, value in sorted(environ.items())
    ]

    response_body = '\n'.join(response)

    status = '200 OK'

    response_headers = [
        ('Content-type', 'text/plain'),
    ]

    start_response(status, response_headers)

    return [response_body.encode('utf-8')]


server = make_server('localhost', 8000, app=Routeware(application))
server.serve_forever()

