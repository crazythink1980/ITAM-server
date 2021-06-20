from marshmallow import fields

from .model import Asset, AssetType
from app.db import db, marshmallow


class AssetTypeSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = AssetType
        load_instance = True


class AssetSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Asset
        load_instance = True

    id = fields.Integer(dump_only=True)
    code = fields.String(required=True)
    name = fields.String(required=True)
    type_id = fields.Integer(required=True)
    created = fields.String(dump_only=True)
    type = fields.Nested(AssetTypeSchema, only=['name'])
