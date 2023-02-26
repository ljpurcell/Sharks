from flask import Blueprint
from flask_login import login_manager


auth = Blueprint('auth', __name__)

from . import views