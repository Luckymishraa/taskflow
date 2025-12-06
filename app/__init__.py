from flask import Flask
from .config import DevelopmentConfig
from .extensions import db, migrate


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/api/health")
    def health():
        return {"status": "ok"}, 200

    return app
