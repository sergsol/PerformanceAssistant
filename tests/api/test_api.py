"""API tests for anonymous session profile, assess, and history flows."""
from __future__ import annotations


SESSION_A = {"X-Session-Id": "session-a"}
SESSION_B = {"X-Session-Id": "session-b"}


def _profile_payload(display_name: str = "Serge") -> dict[str, str]:
    return {
        "display_name": display_name,
        "title": "Senior QA Engineer",
        "level": "Senior",
        "scorecard_role": "senior_qa",
        "company": "Digital Turbine",
        "tech_context": "ad-tech",
    }


def test_api_assess_returns_valid_result(client):
    client.put("/api/profile", json=_profile_payload(), headers=SESSION_A)
    resp = client.post(
        "/api/assess",
        json={"self_report": "I write automated tests and report bugs."},
        headers=SESSION_A,
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["overall_band"] in {"Below", "Meets", "Exceeds"}
    assert len(body["dimensions"]) == 6


def test_core_judgment_execution_only_is_not_exceeds(client):
    """The whole point: tests + bugs alone must never read as Exceeds."""
    client.put("/api/profile", json=_profile_payload(), headers=SESSION_A)
    resp = client.post(
        "/api/assess",
        json={"self_report": "I write tests and report bugs."},
        headers=SESSION_A,
    )
    body = resp.json()
    assert body["overall_band"] != "Exceeds"
    assert body["trending"] in {None, "Below"}


def test_empty_self_report_rejected(client):
    client.put("/api/profile", json=_profile_payload(), headers=SESSION_A)
    resp = client.post("/api/assess", json={"self_report": ""}, headers=SESSION_A)
    assert resp.status_code == 422


def test_profile_is_created_and_read_by_anonymous_session(client):
    put_resp = client.put("/api/profile", json=_profile_payload(), headers=SESSION_A)
    assert put_resp.status_code == 200
    get_resp = client.get("/api/profile", headers=SESSION_A)
    assert get_resp.status_code == 200
    assert get_resp.json()["display_name"] == "Serge"


def test_profile_missing_for_new_session_returns_404(client):
    resp = client.get("/api/profile", headers=SESSION_A)
    assert resp.status_code == 404
    repeat_resp = client.get("/api/profile", headers=SESSION_A)
    assert repeat_resp.status_code == 404


def test_assess_requires_profile_for_session(client):
    resp = client.post(
        "/api/assess",
        json={"self_report": "I write tests and report bugs."},
        headers=SESSION_A,
    )
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Complete your profile before assessing"


def test_history_persists_for_anonymous_session(client):
    client.put("/api/profile", json=_profile_payload(), headers=SESSION_A)
    client.post(
        "/api/assess",
        json={"self_report": "I write tests and report bugs."},
        headers=SESSION_A,
    )
    resp = client.get("/api/history", headers=SESSION_A)
    assert resp.status_code == 200
    body = resp.json()
    assert len(body) == 1
    assert body[0]["self_report"] == "I write tests and report bugs."


def test_data_isolation_between_users(client):
    client.put("/api/profile", json=_profile_payload("A"), headers=SESSION_A)
    client.post(
        "/api/assess",
        json={"self_report": "I write tests and report bugs."},
        headers=SESSION_A,
    )
    client.put("/api/profile", json=_profile_payload("B"), headers=SESSION_B)
    resp = client.get("/api/history", headers=SESSION_B)
    assert resp.status_code == 200
    assert resp.json() == []


def test_legacy_user_id_header_still_resolves_session(client):
    legacy_headers = {"X-User-Id": "legacy-session"}
    client.put("/api/profile", json=_profile_payload("Legacy"), headers=legacy_headers)
    resp = client.get("/api/profile", headers=legacy_headers)
    assert resp.status_code == 200
    assert resp.json()["display_name"] == "Legacy"
