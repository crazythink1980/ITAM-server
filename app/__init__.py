from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config

cors = CORS()
jwt = JWTManager()


def create_app():
    from . import db, utils, assets, dept, users
    app = Flask(__name__)
    app.config.from_object(Config)
    cors.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    utils.init_app(app)
    assets.init_app(app)
    dept.init_app(app)
    users.init_app(app)
    app.logger.info('Flask Rest Api startup')
    return app
