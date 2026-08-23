"""API + auth + data-isolation tests. LLM is stubbed (see conftest)."""
from __future__ import annotations


def test_api_assess_returns_valid_result(client):
    resp = client.post("/api/assess", json={
        "title": "Senior QA Engineer", "level": "Senior",
        "self_report": "I write automated tests and report bugs.",
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["overall_band"] in {"Below", "Meets", "Exceeds"}
    assert len(body["dimensions"]) == 6


def test_core_judgment_execution_only_is_not_exceeds(client):
    """The whole point: tests + bugs alone must never read as Exceeds."""
    resp = client.post("/api/assess", json={
        "title": "Senior QA Engineer", "level": "Senior",
        "self_report": "I write tests and report bugs.",
    })
    body = resp.json()
    assert body["overall_band"] != "Exceeds"
    assert body["trending"] == "Below"


def test_empty_self_report_rejected(client):
    resp = client.post("/api/assess", json={
        "title": "Senior QA Engineer", "level": "Senior", "self_report": "",
    })
    assert resp.status_code == 422


def test_home_requires_login(client):
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code in (303, 307)
    assert "/login" in resp.headers["location"]


def test_wrong_password_rejected(client):
    client.post("/register", data={"email": "u@x.com", "password": "right"},
                follow_redirects=False)
    client.post("/logout", follow_redirects=False)
    resp = client.post("/login", data={"email": "u@x.com", "password": "wrong"})
    assert resp.status_code == 401


def test_duplicate_registration_conflicts(client):
    client.post("/register", data={"email": "dup@x.com", "password": "pw"},
                follow_redirects=False)
    resp = client.post("/register", data={"email": "dup@x.com", "password": "pw"})
    assert resp.status_code == 409


def test_history_persists_after_assess(registered_client):
    registered_client.post("/assess", data={"self_report": "I write tests and report bugs."})
    resp = registered_client.get("/history")
    assert resp.status_code == 200
    assert "trending" in resp.text.lower() or "Meets" in resp.text


def test_data_isolation_between_users(client):
    # User A registers, sets profile, creates an assessment.
    client.post("/register", data={"email": "a@x.com", "password": "pw"}, follow_redirects=False)
    client.post("/profile", data={"display_name": "A", "title": "Senior QA Engineer",
                                  "level": "Senior", "company": "", "tech_context": ""},
                follow_redirects=False)
    client.post("/assess", data={"self_report": "I write tests and report bugs."})
    client.post("/logout", follow_redirects=False)

    # User B registers fresh; their history must be empty (cannot see A's).
    client.post("/register", data={"email": "b@x.com", "password": "pw"}, follow_redirects=False)
    client.post("/profile", data={"display_name": "B", "title": "Senior QA Engineer",
                                  "level": "Senior", "company": "", "tech_context": ""},
                follow_redirects=False)
    resp = client.get("/history")
    assert resp.status_code == 200
    assert "No assessments yet" in resp.text
