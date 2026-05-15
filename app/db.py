import sqlite3
from pathlib import Path

from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    app_root = Path(__file__).resolve().parent.parent
    instance_path = app_root / "instance"
    instance_path.mkdir(exist_ok=True)

    db_path = instance_path / "incident_assistant.sqlite"
    connection = sqlite3.connect(db_path)

    with connection:
        connection.executescript((app_root / "schema.sql").read_text())
        connection.executescript((app_root / "seed.sql").read_text())

    connection.close()


def init_app(app):
    app.teardown_appcontext(close_db)
