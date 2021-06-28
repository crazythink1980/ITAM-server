from marshmallow import fields, post_dump

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

    @post_dump(pass_many=True)
    def modify_place_dump(self, data, many):
        if many:
            for data_obj in data:
                fullname = ''
                parent_ids = []
                parent_obj = data_obj.get('parent')

                while parent_obj is not None:
                    fullname = parent_obj['name'] + '/' + fullname
                    parent_ids.append(parent_obj['id'])
                    parent_obj = parent_obj.get('parent')

                fullname = fullname + data_obj['name']
                parent_ids.append(0)
                parent_ids.reverse()
                data_obj['fullname'] = fullname
                data_obj['parent_ids'] = parent_ids
                data_obj.pop('parent')

                # 将chidren转为hasChildren
                if data_obj['children']:
                    hasChildren = True
                else:
                    hasChildren = False
                data_obj['hasChildren'] = hasChildren
                data_obj.pop('children')
        else:
            # 将parent对象转为fullname和parent_ids
            fullname = ''
            parent_ids = []
            parent_obj = data.get('parent')
            while parent_obj is not None:
                fullname = parent_obj['name'] + '/' + fullname
                parent_ids.append(parent_obj['id'])
                parent_obj = parent_obj.get('parent')
            fullname = fullname + data['name']
            parent_ids.append(0)
            parent_ids.reverse()
            data['fullname'] = fullname
            data['parent_ids'] = parent_ids
            data.pop('parent')

            # 将chidren转为hasChildren
            if data['children']:
                hasChildren = True
            else:
                hasChildren = False
            data['hasChildren'] = hasChildren
            data.pop('children')

        return data
