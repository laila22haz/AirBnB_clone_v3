#!/usr/bin/python3
""" state doc"""

from models.base_model import BaseModel
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import State
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """doc fuction"""
    users_list = []
    users = storage.all(User).values()
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """get users"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ doc delete"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """doc create"""
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Not a JSON')
    if 'email' not in request_data:
        abort(400, 'Missing email')
    if 'password' not in request_data:
        abort(400, 'Missing password')
    new_user = User(**request_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """doc update"""
    put_req = request.get_json()
    if not put_req:
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']

    for key, value in put_req.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return make_response(user.to_dict(), 200)
