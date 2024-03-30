#!/usr/bin/python3
"""This module initializes the application's blueprint"""


from flask import Blueprint


app_views = Blueprint('/app/v1', __name__)

from api.v1.views.index import *
from api.v1.views import states
