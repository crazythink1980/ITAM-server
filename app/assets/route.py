from flask import Blueprint, request
from .model import Asset, AssetType
from .schema import AssetSchema, AssetTypeSchema
from app.utils.responses import response_with
from app.utils import responses as resp
from app.db import db

assets_bp = Blueprint('assets', __name__)


@assets_bp.route('/', methods=['POST'])
def create_asset():
    try:
        data = request.get_json()
        print(data)
        asset_schema = AssetSchema()
        asset = asset_schema.load(data)
        result = asset_schema.dump(asset.create())
        return response_with(resp.SUCCESS_201, value={"asset": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@assets_bp.route('/', methods=['GET'])
def get_aasset_list():
    fetched = Asset.query.all()
    asset_schema = AssetSchema(many=True, only=['code', 'name', 'id', 'type'])
    assets = asset_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"assets": assets})


@assets_bp.route('/<int:asset_id>', methods=['GET'])
def get_asset_detail(asset_id):
    fetched = Asset.query.get_or_404(asset_id)
    asset_schema = AssetSchema()
    asset = asset_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"asset": asset})


@assets_bp.route('/<int:id>', methods=['PUT'])
def update_asset_detail(id):
    data = request.get_json()
    get_asset = Asset.query.get_or_404(id)
    get_asset.code = data['code']
    get_asset.name = data['name']
    get_asset.type_id = data['type_id']
    db.session.add(get_asset)
    db.session.commit()
    asset_schema = AssetSchema()
    asset = asset_schema.dump(get_asset)
    return response_with(resp.SUCCESS_200, value={"asset": asset})


@assets_bp.route('/<int:id>', methods=['PATCH'])
def modify_asset_detail(id):
    data = request.get_json()
    get_asset = Asset.query.get(id)
    if data.get('code'):
        get_asset.name = data['code']
    if data.get('name'):
        get_asset.name = data['name']
    if data.get('type_id'):
        get_asset.last_name = data['type_id']

    db.session.add(get_asset)
    db.session.commit()
    asset_schema = AssetSchema()
    asset = asset_schema.dump(get_asset)
    return response_with(resp.SUCCESS_200, value={"asset": asset})


@assets_bp.route('/<int:id>', methods=['DELETE'])
def delete_asset(id):
    get_asset = Asset.query.get_or_404(id)
    db.session.delete(get_asset)
    db.session.commit()
    return response_with(resp.SUCCESS_204)


@assets_bp.route('/assettype', methods=['POST'])
def create_asset_type():
    try:
        data = request.get_json()
        print(data)
        asset_type_schema = AssetTypeSchema()
        asset_type = asset_type_schema.load(data)
        result = asset_type_schema.dump(asset_type.create())
        return response_with(resp.SUCCESS_201, value={"asset_type": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@assets_bp.route('/assettype', methods=['GET'])
def get_asset_type_list():
    id = request.args.get("id")
    parent_id = request.args.get("parent_id")
    if id is not None:
        fetched = AssetType.query.filter_by(id=id).all()
    else:
        if parent_id is not None:
            fetched = AssetType.query.filter_by(parent_id=parent_id).all()
        else:
            fetched = AssetType.query.all()

    asset_type_schema = AssetTypeSchema(many=True)
    result = asset_type_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"asset_type": result})
