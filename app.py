from flask.helpers import get_debug_flag

from backend import create_app
from backend.config import DevConfig, ProdConfig


CONFIG = DevConfig if get_debug_flag() else ProdConfig


app = create_app(CONFIG)
