from marshmallow import fields

from .model import Asset, Computer
from app.db import marshmallow


class AssetSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Asset
        load_instance = True

    id = fields.Integer(dump_only=True)


class ComputerSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Computer
        load_instance = True

    id = fields.Integer(dump_only=True)