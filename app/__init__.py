import os
from flask import Flask
from .config import DevelopmentConfig, ProductionConfig

from .extensions import db, migrate
from .models import Task, TaskRun
from app.api.tasks import api_bp


def create_app():
    env = os.environ.get("FLASK_ENV", "development")
    config_class = ProductionConfig if env == "production" else DevelopmentConfig
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    app.register_blueprint(api_bp)

    @app.route("/api/health")
    def health():
        return {"status": "ok"}, 200
    return app
