from flask import Blueprint, request
from .model import Asset, Computer, Printer, Server, NetDevice, SecDevice
from .schema import AssetSchema, ComputerSchema, PrinterSchema, ServerSchema, NetDeviceSchema, SecDeviceSchema
from app.utils.responses import response_with
from app.utils import responses as resp
from app.db import db

assets_bp = Blueprint('assets', __name__)
asset_types = {
    'PC': Computer,
    'Printer': Printer,
    'Server': Server,
    'NetDevice': NetDevice,
    'SecDevice': SecDevice
}
asset_type_schemas = {
    'PC': ComputerSchema,
    'Printer': PrinterSchema,
    'Server': ServerSchema,
    'NetDevice': NetDeviceSchema,
    'SecDevice': SecDeviceSchema
}


@assets_bp.route('/assets', methods=['POST'])
def create_asset():
    try:
        data = request.get_json()
        asset_schema = asset_type_schemas.get(data["type"], AssetSchema)()
        asset = asset_schema.load(data)
        print(asset)
        db.session.add(asset)
        db.session.commit()
        result = asset_schema.dump(asset)
        return response_with(resp.SUCCESS_201, value={"data": result})
    except Exception as e:
        print(e)
        db.session.rollback()
        return response_with(resp.INVALID_INPUT_422)


@assets_bp.route('/assets', methods=['GET'])
def get_aasset_list():
    type = request.args.get("type")
    pageSize = request.args.get('pageSize', 10, type=int)  # 每页条数，默认10条
    pageNum = request.args.get('pageNum', 1, type=int)  # 当前分页，默认第一页
    asset = asset_types.get(type, Asset)
    asset_schema = asset_type_schemas.get(type, AssetSchema)(many=True)
    pagination = asset.query.order_by(asset.create_time.desc()).paginate(
        pageNum, per_page=pageSize, error_out=False)

    result = asset_schema.dump(pagination.items)
    return response_with(resp.SUCCESS_200,
                         value={
                             "data": {
                                 "PageSize": pageSize,
                                 "PageNum": pageNum,
                                 "total": pagination.total,
                                 "pages": pagination.pages,
                                 "list": result
                             }
                         })


@assets_bp.route('/assets', methods=['PUT'])
def update_asset():
    data = request.get_json()
    id = data["id"]
    type = data["type"]
    asset = asset_types.get(type, Asset)
    asset_schema = asset_type_schemas.get(type, AssetSchema)()
    try:
        update_asset = asset.query.get(id)
        if update_asset is not None:
            update_asset.update(data)
            db.session.commit()
            result = asset_schema.dump(update_asset)
            return response_with(resp.SUCCESS_200, value={"data": result})
        else:
            return response_with(resp.INVALID_INPUT_422,
                                 message="Update record no found.")
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422,
                             message="Update record Error.")


@assets_bp.route('/assets', methods=['DELETE'])
def delete_asset():
    data = request.get_json()
    id = data["id"]
    get_asset = Asset.query.get_or_404(id)
    db.session.delete(get_asset)
    db.session.commit()
    return response_with(resp.SUCCESS_200, message='Record has been delete.')


@assets_bp.route('/assets/detail', methods=['GET'])
def get_asset_detail():
    id = request.args.get("id")
    if id is not None:
        fetched = Asset.query.get(id)
        if fetched is not None:
            asset_schema = asset_type_schemas.get(fetched.type, AssetSchema)()
            result = asset_schema.dump(fetched)
            return response_with(resp.SUCCESS_200, value={"data": result})
        else:
            return response_with(resp.INVALID_INPUT_422,
                                 message="Record is not found.")
    else:
        return response_with(resp.INVALID_INPUT_422, message="Miss id param.")
