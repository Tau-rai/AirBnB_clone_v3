#!/usr/bin/python3
"""City API views module"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_state_cities(state_id):
    """Retrieve all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """Retrieve a specific City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Create a new City object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    if 'name' not in req_json:
        abort(400, "Missing name")

    new_city = City(**req_json)
    new_city.state_id = state.id
    req_json['state_id'] = state_id
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore_keys:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
