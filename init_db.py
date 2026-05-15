from pathlib import Path

from app.db import init_db


if __name__ == "__main__":
    init_db()
    db_path = Path("instance") / "incident_assistant.sqlite"
    print(f"Database initialized at {db_path}")
