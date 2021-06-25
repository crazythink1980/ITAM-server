from marshmallow import fields, pre_dump

from .model import Asset, AssetType, Computer
from app.db import db, marshmallow


class AssetTypeSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = AssetType
        load_instance = True
        #include_relationships = True

    id = fields.Integer(dump_only=True)
    hasChildren = fields.Boolean(dump_only=True)
    parent_id = fields.Integer()
    #children = fields.Nested('self')

    @pre_dump
    def pre_dump(self, data, **kwargs):
        if data.children != []:
            data.hasChildren = True
        else:
            data.hasChildren = False
        return data


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