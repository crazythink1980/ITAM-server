from marshmallow import fields

from .model import User
from app.db import db, marshmallow


class User_Schema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
