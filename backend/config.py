# -*- coding: utf-8 -*-
"""Application configuration."""
import os


def get_database_connection_uri():
    try:
        flag = os.environ['PY_TEST']
        if flag == '1':
            return 'sqlite://'
    except:
        pass

    user = os.getenv('POSTGRES_USER', '')
    password = os.getenv('POSTGRES_PASSWORD', '')
    host = os.getenv('POSTGRES_HOST', '')
    database = os.getenv('POSTGRES_DB', '')
    port = os.getenv('POSTGRES_PORT', '')

    return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'


class Config(object):
    """Base configuration"""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = get_database_connection_uri()


class ProdConfig(Config):
    """Production Confifuration"""

    ENV = 'prod'
    DEBUG = False


class DevConfig(Config):
    """Development Configuration"""

    ENV = 'dev'
    DEBUG = True


class TestConfig(Config):
    """Testing Configuration"""

    TESTING = True
    DEBUG = True
