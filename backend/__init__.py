from flask import Flask
from flask_cors import CORS, cross_origin

from swagger_ui import api_doc

from backend.config import ProdConfig
from backend.extension import db, migrate, ma


def create_app(config_object=ProdConfig):
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)

    CORS(app)

    api_doc(app, config_path='./doc.yaml', url_prefix='/api/doc', title='API doc')

    register_extensions(app)
    register_blueprints(app)

    app.app_context().push()

    from backend.models.battery import Battery

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)


def register_blueprints(app):
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp, url_prefix='/api')
