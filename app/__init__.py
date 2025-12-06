from flask import Flask
from .config import DevelopmentConfig
from .extensions import db, migrate
from .models import Task, TaskRun


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    return app
