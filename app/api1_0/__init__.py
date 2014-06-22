from flask import Blueprint

api1_0 = Blueprint('api1_0', __name__)

from . import views


