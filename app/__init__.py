from flask import Flask
from pathlib import Path


def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="views/templates",
        static_folder="views/static",
    )
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config.from_mapping(
        DATABASE=app.instance_path + "/incident_assistant.sqlite",
        SECRET_KEY="dev",
    )

    from . import db

    db.init_app(app)

    from .controllers.main_controller import bp

    app.register_blueprint(bp)

    return app
