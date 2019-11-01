from flask import Blueprint

guide = Blueprint('guide', __name__)

from . import adminPages