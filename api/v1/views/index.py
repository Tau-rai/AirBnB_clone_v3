#!/usr/bin/python3
"""This module is the entry point to the flask app"""


from api.v1.views import app_views
from flask import jsonify
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Ameniyty
from models import storage
from storage import count




classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('/status')
def status():
    """Defines the status of a request"""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def get_stats():
    stats = {}
    for cls_name, cls_object in classes.items():
        count = storage.count(cls_name)
        stats[cls_name] = count
    return jsonify(stats), 200
