#!/usr/bin/python3
"""This module is the entry point to the flask app"""


from api.v1.views import app_views
from flask import jsonify
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity
from models import storage


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status')
def status():
    """Defines the status of a request"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Retreives the number of each object by type"""
    counts = {}
    for cls_name, cls_obj in classes.items():
        counts[cls_name] = storage.count(cls_obj)
    return jsonify(counts)
