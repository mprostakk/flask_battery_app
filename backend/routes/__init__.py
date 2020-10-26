from flask import Blueprint


bp = Blueprint('routes', __name__)


from backend.routes.battery import *
from backend.routes.charge import *
from backend.routes.chargemeasurement import *
