from flask import Blueprint
from flask_login import login_manager
from .models.user import User

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

from . import views