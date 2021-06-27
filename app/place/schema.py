from marshmallow import fields

from .model import Place
from app.db import marshmallow


class PlaceSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Place
        load_instance = True
        include_relationships = True

    id = fields.Integer(dump_only=True)
    parent_id = fields.Integer()
    parent = fields.Nested('self')
    # children = fields.Nested('self')
