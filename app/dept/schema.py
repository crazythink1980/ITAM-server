from marshmallow import fields, pre_dump

from .model import Dept
from app.db import marshmallow


class DeptSchema(marshmallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Dept
        load_instance = True
        # include_relationships = True

    id = fields.Integer(dump_only=True)
    hasChildren = fields.Boolean(dump_only=True)
    parent_id = fields.Integer()
    # children = fields.Nested('self')

    @pre_dump
    def pre_dump(self, data, **kwargs):
        if data.children != []:
            data.hasChildren = True
        else:
            data.hasChildren = False
        return data
