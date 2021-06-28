from marshmallow import fields, post_dump

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

    # @post_dump()
    # def add_place_name(self, data, **kwargs):
    #     place_name = ''
    #     place_id = []
    #     if data['place_obj']:
    #         place_obj = data['place_obj']
    #         while place_obj:
    #             place_name = place_obj['name'] + '/' + place_name
    #             place_id.append(place_obj['id'])
    #             place_obj = place_obj['parent']
    #         place_id.append(0)
    #         place_id.reverse()
    #         data['place_name'] = place_name[0:-1]
    #         data['place_id'] = place_id
    #         data.pop('place_obj')
    #     return data


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
