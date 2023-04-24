from flask import Blueprint

auth = Blueprint('auth', __name__)

from ..main import errors
from . import views