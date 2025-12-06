import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///taskflow.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "dev-secret"
