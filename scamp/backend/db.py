# backend/db.py

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional, Dict

DB_PATH = Path(__file__).resolve().parent / "scamp.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                platform TEXT NOT NULL,
                media_type TEXT NOT NULL,
                score REAL NOT NULL,
                label TEXT NOT NULL,
                file_path TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_event(
    user_id: str,
    platform: str,
    media_type: str,
    score: float,
    label: str,
    file_path: str,
) -> int:
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO events (user_id, platform, media_type, score, label, file_path)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, platform, media_type, float(score), label, file_path),
        )
        conn.commit()
        return int(cur.lastrowid)
    finally:
        conn.close()


def get_event(event_id: int) -> Optional[Dict]:
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM events WHERE id = ?", (event_id,))
        row = cur.fetchone()
    finally:
        conn.close()

    if row is None:
        return None

    return dict(row)
