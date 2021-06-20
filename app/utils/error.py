import logging
from .responses import response_with, SERVER_ERROR_404, SERVER_ERROR_500, BAD_REQUEST_400


def register_errors(app):
    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(SERVER_ERROR_404)

    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(SERVER_ERROR_500)

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(BAD_REQUEST_400)
