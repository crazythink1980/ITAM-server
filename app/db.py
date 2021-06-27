from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
marshmallow = Marshmallow()


def init_app(app):
    db.init_app(app)
    marshmallow.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
