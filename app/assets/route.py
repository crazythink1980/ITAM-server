from flask import Blueprint, request
from .model import Asset, Computer
from .schema import AssetSchema, ComputerSchema
from app.utils.responses import response_with
from app.utils import responses as resp
from app.db import db

assets_bp = Blueprint('assets', __name__)
asset_types = {1: Computer}
asset_type_schemas = {1: ComputerSchema}


@assets_bp.route('/assets', methods=['POST'])
def create_asset():
    try:
        data = request.get_json()
        print(data)
        asset_schema = asset_type_schemas.get(int(data["type"]), AssetSchema)()
        asset = asset_schema.load(data)
        db.session.add(asset)
        db.session.commit()
        result = asset_schema.dump(asset)
        return response_with(resp.SUCCESS_201, value={"data": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@assets_bp.route('/assets', methods=['GET'])
def get_aasset_list():
    type = request.args.get("type")
    if type is not None:
        type = int(type)
    else:
        type = 0
    asset = asset_types.get(int(type), Asset)
    asset_schema = asset_type_schemas.get(int(type), AssetSchema)(many=True)
    fetched = asset.query.all()
    print(asset_schema)
    print(fetched)
    assets = asset_schema.dump(fetched)
    print(assets)
    return response_with(resp.SUCCESS_200, value={"data": assets})


@assets_bp.route('/assets/detail', methods=['GET'])
def get_asset_detail():
    id = request.args.get("id")
    if id is not None:
        fetched = Asset.query.filter_by(id=id).first()
        asset_schema = asset_type_schemas.get(fetched.type, AssetSchema)()
        asset = asset_schema.dump(fetched)
        return response_with(resp.SUCCESS_200, value={"data": asset})
    else:
        return response_with(resp.INVALID_INPUT_422, message="miss id")


# @assets_bp.route('/assets/<int:id>', methods=['PUT'])
# def update_asset_detail(id):
#     data = request.get_json()
#     get_asset = Asset.query.get_or_404(id)
#     get_asset.code = data['code']
#     get_asset.name = data['name']
#     get_asset.type_id = data['type_id']
#     db.session.add(get_asset)
#     db.session.commit()
#     asset_schema = AssetSchema()
#     asset = asset_schema.dump(get_asset)
#     return response_with(resp.SUCCESS_200, value={"asset": asset})

# @assets_bp.route('/assets/<int:id>', methods=['PATCH'])
# def modify_asset_detail(id):
#     data = request.get_json()
#     get_asset = Asset.query.get(id)
#     if data.get('code'):
#         get_asset.name = data['code']
#     if data.get('name'):
#         get_asset.name = data['name']
#     if data.get('type_id'):
#         get_asset.last_name = data['type_id']

#     db.session.add(get_asset)
#     db.session.commit()
#     asset_schema = AssetSchema()
#     asset = asset_schema.dump(get_asset)
#     return response_with(resp.SUCCESS_200, value={"asset": asset})

# @assets_bp.route('/assets/<int:id>', methods=['DELETE'])
# def delete_asset(id):
#     get_asset = Asset.query.get_or_404(id)
#     db.session.delete(get_asset)
#     db.session.commit()
#     return response_with(resp.SUCCESS_204)
