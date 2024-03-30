#!/usr/bin/python3
"""This modules handles the api for states"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/states', method= 'GET')
def states():
    """Retrieves all the state objects"""
    all_objs = storage.all()
    for obj in all_objs.values():
        if obj.name == obj.__name__:
