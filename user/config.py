import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEVELOPMENT = True
    DEBUG = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@postgres:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
