from flask import Blueprint

knowledge_structure = Blueprint('knowledge_structure', __name__)

from . import views
