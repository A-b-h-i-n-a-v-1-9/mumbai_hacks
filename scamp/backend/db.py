import sqlite3
from pathlib import Path
from datetime import datetime

# Path to scamp.db in project root
DB_PATH = Path(__file__).resolve().parent.parent / "scamp.db"


def get_conn():
    """Return a new SQLite connection."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Initialize SQLite with basic tables for events and feedback.
    Safe to call multiple times.
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            platform TEXT,
            media_type TEXT,
            score REAL,
            label TEXT,
            created_at TEXT,
            file_path TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            user_id TEXT,
            feedback TEXT,
            created_at TEXT
        )
        """
    )

    conn.commit()
    conn.close()


def save_event(user_id: str,
               platform: str,
               media_type: str,
               score: float,
               label: str,
               file_path: str) -> int:
    """
    Insert a new scan event and return its ID.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO events (user_id, platform, media_type, score, label, created_at, file_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, platform, media_type, score, label, datetime.utcnow().isoformat(), file_path),
    )
    conn.commit()
    event_id = cur.lastrowid
    conn.close()
    return event_id


def save_feedback(event_id: int, user_id: str, feedback: str) -> None:
    """
    Store user feedback for a given event.
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO feedback (event_id, user_id, feedback, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (event_id, user_id, feedback, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()
