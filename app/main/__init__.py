from flask import Blueprint

main = Blueprint('main', __name__)
api = Blueprint('api', __name__)

from . import views, errors