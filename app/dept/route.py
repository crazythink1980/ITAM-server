from flask import Blueprint, request
from .model import Dept
from .schema import DeptSchema
from app.utils.responses import response_with
from app.utils import responses as resp
from app.db import db

dept_bp = Blueprint('dept', __name__)


@dept_bp.route('/dept', methods=['POST'])
def create_asset_type():
    try:
        data = request.get_json()
        dept_schema = DeptSchema()
        dept = dept_schema.load(data)
        result = dept_schema.dump(dept.create())
        return response_with(resp.SUCCESS_201, value={"data": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@dept_bp.route('/dept', methods=['GET'])
def get_asset_type_list():
    parent_id = request.args.get("parent_id")

    if parent_id is not None:
        fetched = Dept.query.filter_by(parent_id=parent_id).all()
    else:
        fetched = Dept.query.all()

    dept_schema = DeptSchema(many=True)
    result = dept_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"data": result})


@dept_bp.route('/dept', methods=['PUT'])
def update_asset_type():
    data = request.get_json()
    dept = Dept.query.get_or_404(data['id'])
    dept.name = data['name']
    dept.parent_id = data['parent_id']
    db.session.add(dept)
    db.session.commit()
    dept_schema = DeptSchema()
    result = dept_schema.dump(dept)
    return response_with(resp.SUCCESS_200, value={"data": result})


@dept_bp.route('/dept', methods=['DELETE'])
def delete_asset_type():
    data = request.get_json()
    dept = Dept.query.get_or_404(data['id'])
    db.session.delete(dept)
    db.session.commit()
    return response_with(resp.SUCCESS_200)
