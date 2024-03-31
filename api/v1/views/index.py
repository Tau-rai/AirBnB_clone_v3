8#!/usr/bin/python3
"""This module is the entry point to the flask app"""


from api.v1.views import app_views
from flask import jsonify
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status', methods=["GET"])
def status():
    """Defines the status of a request"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """Returns the number of items in storage in JSON format"""
    from models import storage
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User
               }

    all_cls_stats = {key: storage.count(val) for key, val in classes.items()}
    return jsonify(all_cls_stats)
