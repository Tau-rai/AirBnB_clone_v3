#!/usr/bin/python3
"""This modules handles the api for places"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places(city_id):
    """Retrieves all the place objects linked to a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_objs = city.places
    places_dict = [place.to_dict() for place in places_objs]
    return jsonify(places_dict)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieves a place with a given ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes an place with a given ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def new_place(city_id):
    """Creates a new place object linked to a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')

    data = request.get_json()
    user_id = data.get('user_id')
    name = data.get('name')

    if not user_id:
        abort(400, description='Missing user_id')
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not name:
        abort(400, description='Missing name')

    # create a new place and save
    new_place = Place(name=name, city_id=city_id, user_id=user_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a place object with a given ID"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    for key, value in request.get_json().items():
        if key not in [
                'id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
