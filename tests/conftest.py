"""Shared fixtures. Tests run against SQLite with a stubbed LLM for speed and
determinism. Live-model behavior is validated separately in evals/.
"""
from __future__ import annotations

import os

# Force test config BEFORE app modules import settings.
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["LLM_PROVIDER"] = "stub"

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


def _register_and_auth(client, email: str, password: str = "testpassword"):
    """Register a user via the API and return (client_with_auth, access_token)."""
    resp = client.post(
        "/api/auth/register",
        json={"email": email, "password": password},
    )
    assert resp.status_code == 201, f"register failed: {resp.status_code} {resp.text}"
    body = resp.json()
    access_token = body["access_token"]
    client.headers["Authorization"] = f"Bearer {access_token}"
    return client, access_token, body.get("refresh_token")


@pytest.fixture
def registered_client(client):
    """A client already registered + logged in, with a profile set.

    Uses the new JWT API. The returned client has an Authorization header
    set so subsequent requests are authenticated.
    """
    client.post(
        "/api/auth/register",
        json={"email": "a@example.com", "password": "testpassword"},
    )
    # Get a fresh token to be safe
    resp = client.post(
        "/api/auth/login",
        json={"email": "a@example.com", "password": "testpassword"},
    )
    assert resp.status_code == 200
    access_token = resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {access_token}"

    client.post(
        "/api/profile",
        json={
            "display_name": "Serge",
            "title": "Senior QA Engineer",
            "level": "Senior",
            "company": "Digital Turbine",
            "tech_context": "ad-tech",
        },
    )
    return client
