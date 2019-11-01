from flask import Blueprint

solutionss = Blueprint('solutionss', __name__)

from . import views
