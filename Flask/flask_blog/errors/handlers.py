from flask import Blueprint

errors = Blueprint('errors', __name__)


@errors.errorhandler(404)
def error(404):

