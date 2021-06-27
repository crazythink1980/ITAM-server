from flask import Blueprint, request
from .model import AssetType
from .schema import AssetTypeSchema
from app.utils.responses import response_with
from app.utils import responses as resp
from app.db import db

asset_type_bp = Blueprint('asset_type', __name__)


@asset_type_bp.route('/assettype', methods=['POST'])
def create_asset_type():
    try:
        data = request.get_json()
        asset_type_schema = AssetTypeSchema()
        asset_type = asset_type_schema.load(data)
        result = asset_type_schema.dump(asset_type.create())
        return response_with(resp.SUCCESS_201, value={"data": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@asset_type_bp.route('/assettype', methods=['GET'])
def get_asset_type_list():
    parent_id = request.args.get("parent_id")
    id = request.args.get("id")

    if id is not None:
        fetched = AssetType.query.filter_by(id=id).first()
        dept_schema = AssetTypeSchema()
    else:
        if parent_id is not None:
            fetched = AssetType.query.filter_by(parent_id=parent_id).all()
            dept_schema = AssetTypeSchema(many=True)
        else:
            return response_with(resp.INVALID_INPUT_422)

    result = dept_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"data": result})


@asset_type_bp.route('/assettype', methods=['PUT'])
def update_asset_type():
    data = request.get_json()
    dept = AssetType.query.get_or_404(data['id'])
    dept.name = data['name']
    dept.parent_id = data['parent_id']
    db.session.add(dept)
    db.session.commit()
    dept_schema = AssetTypeSchema()
    result = dept_schema.dump(dept)
    return response_with(resp.SUCCESS_200, value={"data": result})


@asset_type_bp.route('/assettype', methods=['DELETE'])
def delete_asset_type():
    data = request.get_json()
    dept = AssetType.query.get_or_404(data['id'])
    db.session.delete(dept)
    db.session.commit()
    return response_with(resp.SUCCESS_200)
