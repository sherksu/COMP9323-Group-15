"""
# Project           : COMP9323
# Author            : Heping Zhao
# Date created      : 25/10/2019
# Description       : GUIDE SYSTEM BLUEPRINT
"""

from flask import Blueprint

guide = Blueprint('guide', __name__)

from . import adminPages