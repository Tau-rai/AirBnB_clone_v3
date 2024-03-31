#!/usr/bin/python3
"""This module creates a flask app"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.errorhandler(404)
def not_found(e):
    """"Custom error message"""
    return jsonify({"error": "Not found"})


@app.teardown_appcontext
def close_db(Exception):
    """Closes an instance of storage"""
    storage.close()

if __name__ == "__main__":
    api_host = getenv('HBNB_API_HOST')
    api_port = getenv('HBNB_API_PORT')
    app.run(host=api_host or "0.0.0.0", port=api_port or 5000, threaded=True, debug=True)