"""Engine + session management. The URL comes from settings, so tests use
SQLite and production uses Postgres with no code change.
"""
from __future__ import annotations

from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

from app.settings import get_settings

_settings = get_settings()

# check_same_thread only matters for SQLite; harmless to compute conditionally.
_connect_args = {"check_same_thread": False} if _settings.database_url.startswith("sqlite") else {}

engine = create_engine(_settings.database_url, echo=False, connect_args=_connect_args)


def init_db() -> None:
    """Create tables. In a fuller project this would be Alembic migrations."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
