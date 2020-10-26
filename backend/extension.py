from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy, Model
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
