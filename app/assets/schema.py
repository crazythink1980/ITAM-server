from marshmallow import fields

from .model import Asset, Computer, Printer, Server, NetDevice, SecDevice
from app.db import marshmallow


class AssetSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Asset
        load_instance = True

    id = fields.Integer(dump_only=True)
    manage_user = fields.Integer()
    use_dept = fields.Integer()


class ComputerSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Computer
        load_instance = True

    id = fields.Integer(dump_only=True)
    manage_user = fields.Integer()
    use_dept = fields.Integer()


class PrinterSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Printer
        load_instance = True

    id = fields.Integer(dump_only=True)
    manage_user = fields.Integer()
    use_dept = fields.Integer()


class ServerSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Server
        load_instance = True

    id = fields.Integer(dump_only=True)
    manage_user = fields.Integer()
    use_dept = fields.Integer()


class NetDeviceSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = NetDevice
        load_instance = True

    id = fields.Integer(dump_only=True)
    manage_user = fields.Integer()
    use_dept = fields.Integer()
    product_date = fields.Date()
    expire_date = fields.Date()
    trade_date = fields.Date()


class SecDeviceSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = SecDevice
        load_instance = True

    id = fields.Integer(dump_only=True)
    manage_user = fields.Integer()
    use_dept = fields.Integer()