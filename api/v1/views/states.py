#!/usr/bin/python3
"""This modules handles the api for states"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def states():
    """Retrieves all the state objects"""
    state_objs = storage.all(State).values()
    states_dict = [state.to_dict() for state in state_objs]
    return jsonify(states_dict)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a state with a given ID"""
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            return jsonify(state.to_dict())
    return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state with a given ID"""
    states = storage.all(State).values()
    for state in states:
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return {}, 200
    return abort(404)


@app_views.route('/states', methods=['POST'])
def new_states():
    """Creates a new state object"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    new_state = State(name=request.get_json()['name'])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a state object with a given ID"""
    states = storage.all(State)
    state = next(
        (state for state in states.values() if state.id == state_id), None)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
