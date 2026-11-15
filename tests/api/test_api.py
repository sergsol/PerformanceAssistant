"""API + auth + data-isolation tests. LLM is stubbed (see conftest)."""

from __future__ import annotations


def test_api_assess_returns_valid_result(registered_client):
    resp = registered_client.post(
        "/api/assess",
        json={"self_report": "I write automated tests and report bugs."},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["overall_band"] in {"Below", "Meets", "Exceeds"}
    assert len(body["dimensions"]) == 6


def test_core_judgment_execution_only_is_not_exceeds(registered_client):
    """The whole point: tests + bugs alone must never read as Exceeds."""
    resp = registered_client.post(
        "/api/assess",
        json={"self_report": "I write tests and report bugs."},
    )
    body = resp.json()
    assert body["overall_band"] != "Exceeds"
    assert body["trending"] == "Below"


def test_empty_self_report_rejected(registered_client):
    resp = registered_client.post(
        "/api/assess",
        json={"self_report": ""},
    )
    assert resp.status_code == 422


def test_home_requires_login(client):
    resp = client.get("/api/profile", follow_redirects=False)
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Login required"


def test_wrong_password_rejected(client):
    client.post(
        "/api/auth/register",
        json={"email": "u@x.com", "password": "correcthorse"},
    )
    resp = client.post(
        "/api/auth/login",
        json={"email": "u@x.com", "password": "wrongpassword"},
    )
    assert resp.status_code == 401


def test_duplicate_registration_conflicts(client):
    client.post(
        "/api/auth/register",
        json={"email": "dup@x.com", "password": "password123"},
    )
    resp = client.post(
        "/api/auth/register",
        json={"email": "dup@x.com", "password": "password456"},
    )
    assert resp.status_code == 409


def test_duplicate_registration_is_case_insensitive(client):
    client.post(
        "/api/auth/register",
        json={"email": "Case@X.com", "password": "password123"},
    )
    resp = client.post(
        "/api/auth/register",
        json={"email": "  case@x.COM ", "password": "password456"},
    )
    assert resp.status_code == 409


def test_login_email_is_case_insensitive(client):
    client.post(
        "/api/auth/register",
        json={"email": "mixed@x.com", "password": "password123"},
    )
    resp = client.post(
        "/api/auth/login",
        json={"email": "MIXED@x.com", "password": "password123"},
    )
    assert resp.status_code == 200


def test_register_rejects_invalid_email(client):
    resp = client.post(
        "/api/auth/register",
        json={"email": "not-an-email", "password": "password123"},
    )
    assert resp.status_code == 422


def test_register_rejects_short_password(client):
    resp = client.post(
        "/api/auth/register",
        json={"email": "short@x.com", "password": "short"},
    )
    assert resp.status_code == 422


def test_history_persists_after_assess(registered_client):
    registered_client.post(
        "/api/assess",
        json={"self_report": "I write tests and report bugs."},
    )
    resp = registered_client.get("/api/history")
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) >= 1
    assert items[0]["overall_band"] in {"Below", "Meets", "Exceeds"}


def test_data_isolation_between_users(client):
    # User A registers, sets profile, creates an assessment.
    client.post(
        "/api/auth/register",
        json={"email": "a@x.com", "password": "password123"},
    )
    # Login as A
    resp = client.post(
        "/api/auth/login",
        json={"email": "a@x.com", "password": "password123"},
    )
    a_token = resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {a_token}"

    client.post(
        "/api/profile",
        json={
            "display_name": "A",
            "title": "Senior QA Engineer",
            "level": "Senior",
            "company": "",
            "tech_context": "",
        },
    )
    client.post(
        "/api/assess",
        json={"self_report": "I write tests and report bugs."},
    )

    # User B registers fresh; their history must be empty (cannot see A's).
    client.post(
        "/api/auth/register",
        json={"email": "b@x.com", "password": "password456"},
    )
    resp = client.post(
        "/api/auth/login",
        json={"email": "b@x.com", "password": "password456"},
    )
    b_token = resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {b_token}"

    client.post(
        "/api/profile",
        json={
            "display_name": "B",
            "title": "Senior QA Engineer",
            "level": "Senior",
            "company": "",
            "tech_context": "",
        },
    )
    resp = client.get("/api/history")
    assert resp.status_code == 200
    assert resp.json() == []


# --- Login-free flow ---------------------------------------------------------


def test_assess_works_without_an_account(client):
    resp = client.post(
        "/api/assess",
        json={"self_report": "I run the roadmap.", "scorecard_role": "senior_prodm"},
    )
    assert resp.status_code == 200
    names = [d["dimension"] for d in resp.json()["dimensions"]]
    assert "Discovery & customer insight" in names
    assert len(names) == 6


def test_anonymous_assess_defaults_to_senior_qa(client):
    resp = client.post("/api/assess", json={"self_report": "I write tests and report bugs."})
    assert resp.status_code == 200
    assert resp.json()["dimensions"][0]["dimension"] == "Technical execution & automation"


def test_anonymous_assess_is_not_saved_anywhere(client):
    client.post("/api/assess", json={"self_report": "I write tests.", "scorecard_role": "mid_qa"})
    # History is account-only and an anonymous caller has none.
    assert client.get("/api/history").status_code == 401


def test_unknown_role_rejected(client):
    resp = client.post("/api/assess", json={"self_report": "x", "scorecard_role": "wizard"})
    assert resp.status_code == 422


def test_overlong_self_report_rejected(client):
    resp = client.post("/api/assess", json={"self_report": "a" * 8001})
    assert resp.status_code == 422


def test_assess_is_rate_limited_per_client(monkeypatch):
    from fastapi.testclient import TestClient

    from app.main import create_app
    from app.settings import get_settings

    monkeypatch.setattr(get_settings(), "assess_rate_limit_per_hour", 2)
    limited = TestClient(create_app())
    body = {"self_report": "I write tests."}
    assert limited.post("/api/assess", json=body).status_code == 200
    assert limited.post("/api/assess", json=body).status_code == 200
    assert limited.post("/api/assess", json=body).status_code == 429
