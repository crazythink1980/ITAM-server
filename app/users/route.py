from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required

from app.utils.responses import response_with
from app.utils import responses as resp
from app.db import db

from .model import User
from .schema import User_Schema

users_bp = Blueprint('users', __name__)


@users_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        print(data)
        user_schema = User_Schema()
        data['password'] = User.generate_hash(data['password'])
        user = user_schema.load(data)
        result = user_schema.dump(user.create())
        return response_with(resp.SUCCESS_201, value={"user": result})
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_user_list():
    fetched = User.query.all()
    user_schema = User_Schema(many=True, only=['id', 'login_name', 'username'])
    users = user_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"users": users})


@users_bp.route('/login', methods=['POST'])
def authenticate_user():
    try:
        data = request.get_json()
        current_user = User.find_by_username(data['username'])
        if not current_user:
            return response_with(resp.SERVER_ERROR_404, message='用户名不存在！')
        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            return response_with(resp.SUCCESS_201,
                                 value={
                                     'user': {
                                         "username": current_user.username,
                                         "access_token": access_token
                                     }
                                 })
        else:
            return response_with(resp.UNAUTHORIZED_401, message='密码不正确！')
    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)
