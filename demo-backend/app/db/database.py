import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db.sqlite3"

def get_connection():
    return sqlite3.connect(DB_PATH)
