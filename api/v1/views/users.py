#!/usr/bin/python3
"""User API views module"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieve all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a specific User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """Create a new User object"""
    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    if 'email' not in req_json:
        abort(400, "Missing email")
    if 'password' not in req_json:
        abort(400, "Missing password")

    new_user = User(**req_json)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore_keys:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
