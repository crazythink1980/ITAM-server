from .log import register_logging
from .error import register_errors


def init_app(app):
    register_logging(app)
    register_errors(app)
