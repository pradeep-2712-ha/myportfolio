import sqlite3
from pathlib import Path

from app.core.config import settings


def _sqlite_file_path() -> Path:
    prefix = "sqlite:///"
    if not settings.database_url.startswith(prefix):
        raise ValueError("Only sqlite DATABASE_URL is supported in this setup.")
    return Path(settings.database_url.replace(prefix, "", 1))


def get_db():
    db_path = _sqlite_file_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    db_path = _sqlite_file_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                title TEXT NOT NULL,
                tagline TEXT NOT NULL,
                about TEXT NOT NULL,
                contact_email TEXT NOT NULL,
                location TEXT NOT NULL,
                phone TEXT NOT NULL DEFAULT '',
                linkedin_url TEXT NOT NULL DEFAULT '',
                github_url TEXT NOT NULL DEFAULT ''
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                level TEXT NOT NULL,
                category TEXT NOT NULL,
                portfolio_id INTEGER NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                stack_csv TEXT NOT NULL,
                link TEXT NOT NULL,
                portfolio_id INTEGER NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS experience (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                company TEXT NOT NULL,
                period TEXT NOT NULL,
                highlights_csv TEXT NOT NULL,
                portfolio_id INTEGER NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS education (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                degree TEXT NOT NULL,
                institution TEXT NOT NULL,
                year TEXT NOT NULL,
                portfolio_id INTEGER NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS certifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                issuer TEXT NOT NULL,
                year TEXT NOT NULL,
                portfolio_id INTEGER NOT NULL
            )
            """
        )
        _ensure_portfolio_column(cursor, "phone", "TEXT NOT NULL DEFAULT ''")
        _ensure_portfolio_column(cursor, "linkedin_url", "TEXT NOT NULL DEFAULT ''")
        _ensure_portfolio_column(cursor, "github_url", "TEXT NOT NULL DEFAULT ''")
        conn.commit()
    finally:
        conn.close()


def _ensure_portfolio_column(cursor: sqlite3.Cursor, column_name: str, column_def: str) -> None:
    columns = cursor.execute("PRAGMA table_info(portfolio)").fetchall()
    existing = {row[1] for row in columns}
    if column_name not in existing:
        cursor.execute(f"ALTER TABLE portfolio ADD COLUMN {column_name} {column_def}")
