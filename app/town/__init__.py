from flask import Blueprint

town = Blueprint('town', __name__)

from . import views