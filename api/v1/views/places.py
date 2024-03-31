#!/usr/bin/python3
"""Place API views module"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User

@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_city_places(city_id):
    """Retrieve all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieve a specific Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create a new Place object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")
    if 'user_id' not in req_json:
        abort(400, "Missing user_id")
    if 'name' not in req_json:
        abort(400, "Missing name")

    user_id = req_json['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    new_place = Place(**req_json)
    new_place.city_id = city.id
    new_place.user_id = user.id
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    req_json = request.get_json()
    if req_json is None:
        abort(400, "Not a JSON")

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in req_json.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
