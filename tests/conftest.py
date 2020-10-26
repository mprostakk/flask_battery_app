import pytest

from sqlalchemy.engine import Engine
from sqlalchemy import event

from webtest import TestApp

from app import app as flask_app
from app import create_app
from backend.config import TestConfig
from backend.extension import db as _db


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture
def app():

    _app = create_app(TestConfig)
    with _app.app_context():
        _db.create_all()

    ctx = _app.test_request_context()
    ctx.push()
    yield flask_app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    return TestApp(app)


@pytest.fixture
def client(app):

    # flask_app.config['TESTING'] = True
    # with flask_app.test_client() as client:
    #     with flask_app.app_context():
    #         pass
    #         # flask_app.init_db()
    #     yield client

    return app.test_client()


@pytest.yield_fixture(scope='function')
def db(app):
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()
