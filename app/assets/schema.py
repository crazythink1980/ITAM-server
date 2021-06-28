from marshmallow import fields

from .model import Asset, Computer, Printer, Server, NetDevice, SecDevice
from app.db import marshmallow
from app.place.schema import PlaceSchema


class AssetSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Asset
        load_instance = True
        include_relationships = True

    id = fields.Integer(dump_only=True)
    manage_user = fields.Integer()
    use_dept = fields.Integer()
    place = fields.Integer()
    place_obj = fields.Nested(PlaceSchema, dump_only=True)
    product_date = fields.Date()
    expire_date = fields.Date()
    trade_date = fields.Date()


class ComputerSchema(AssetSchema):
    class Meta:
        model = Computer
        load_instance = True


class PrinterSchema(AssetSchema):
    class Meta:
        model = Printer
        load_instance = True


class ServerSchema(AssetSchema):
    class Meta:
        model = Server
        load_instance = True


class NetDeviceSchema(AssetSchema):
    class Meta:
        model = NetDevice
        load_instance = True


class SecDeviceSchema(AssetSchema):
    class Meta:
        model = SecDevice
        load_instance = True
