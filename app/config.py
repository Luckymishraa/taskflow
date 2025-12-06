import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + \
        os.path.join(BASE_DIR, "taskflow.db")


class ProductionConfig(BaseConfig):
    DEBUG = False
    # For Render/Railway, they usually provide DATABASE_URL; if not, fallback to sqlite
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///taskflow.db")
