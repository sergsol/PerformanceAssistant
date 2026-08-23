"""Shared fixtures. Tests run against SQLite with a stubbed LLM for speed and
determinism. Live-model behavior is validated separately in evals/.
"""
from __future__ import annotations

import os

# Force test config BEFORE app modules import settings.
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["LLM_PROVIDER"] = "stub"
os.environ["SECRET_KEY"] = "test-secret"

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from app.db.session import engine
from app.main import create_app


@pytest.fixture(autouse=True)
def fresh_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client():
    return TestClient(create_app())


@pytest.fixture
def registered_client(client):
    """A client already registered + logged in, with a profile set."""
    client.post("/register", data={"email": "a@example.com", "password": "pw"},
                follow_redirects=False)
    client.post("/profile", data={
        "display_name": "Serge", "title": "Senior QA Engineer",
        "level": "Senior", "company": "Digital Turbine", "tech_context": "ad-tech",
    }, follow_redirects=False)
    return client
