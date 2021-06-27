from flask import Blueprint, request
from .model import Place
from .schema import PlaceSchema
from app.utils.responses import response_with
from app.utils import responses as resp
from app.db import db

place_bp = Blueprint('place', __name__)


@place_bp.route('/place', methods=['POST'])
def create_place():
    try:
        data = request.get_json()

        place = Place(data["name"])

        if (data["parent_id"] != 0):
            parentPlace = Place.query.get_or_404(data['parent_id'])
            place.parent = parentPlace

        place_schema = PlaceSchema(only=('id', 'name', 'parent_id'))
        result = place_schema.dump(place.create())
        return response_with(resp.SUCCESS_201, value={"data": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@place_bp.route('/place', methods=['GET'])
def get_place_list():
    parent_id = request.args.get("parent_id")
    id = request.args.get("id")

    if id is not None:
        fetched = Place.query.filter_by(id=id).first()
        place_schema = PlaceSchema(only=('id', 'name', 'parent_id', 'parent'))
    else:
        if parent_id is not None:
            fetched = Place.query.filter_by(parent_id=parent_id).all()
            place_schema = PlaceSchema(many=True,
                                       only=('id', 'name', 'parent_id',
                                             'children'))
        else:
            return response_with(resp.INVALID_INPUT_422)

    result = place_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"data": result})


@place_bp.route('/place', methods=['PUT'])
def update_asset_type():
    data = request.get_json()
    place = Place.query.get_or_404(data['id'])
    place.name = data['name']
    place.parent_id = data['parent_id']
    db.session.add(place)
    db.session.commit()
    place_schema = PlaceSchema()
    result = place_schema.dump(place)
    return response_with(resp.SUCCESS_200, value={"data": result})


@place_bp.route('/place', methods=['DELETE'])
def delete_place():
    data = request.get_json()
    place = Place.query.get_or_404(data['id'])
    db.session.delete(place)
    db.session.commit()
    return response_with(resp.SUCCESS_200)
