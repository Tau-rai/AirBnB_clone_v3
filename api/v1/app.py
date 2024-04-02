#!/usr/bin/python3
"""This module creates a flask app"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.errorhandler(404)
def not_found(error):
    """"Custom error message"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_db(Exception):
    """Closes an instance of storage"""
    storage.close()


if __name__ == "__main__":
    api_host = getenv('HBNB_API_HOST', '0.0.0.0')
    api_port = getenv('HBNB_API_PORT', 5000)
    app.run(host=api_host, port=api_port, threaded=True, debug=True)
