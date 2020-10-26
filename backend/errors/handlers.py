from flask import request

from backend.errors import bp
from backend import db


@bp.app_errorhandler(500)
def internal_error(error):
    return {500: 'error'}
