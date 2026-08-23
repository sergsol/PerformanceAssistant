"""End-to-end UI tests (Phase 6). Marked 'ui' so they run in a dedicated CI
stage that has a browser + a running server.

Run locally:
    LLM_PROVIDER=stub uvicorn app.main:app --port 8000 &
    playwright install chromium
    pytest -m ui --base-url http://localhost:8000
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.ui

BASE = "http://localhost:8000"
EMAIL = "ui_test@example.com"
PASSWORD = "testpass123"


@pytest.fixture(scope="session")
def registered_user(browser):
    """Register the shared test user once; delete them from the DB on teardown.

    This means every full test run starts clean and the user can be re-created
    on the next run without a 409 conflict.
    """
    import sqlite3
    from pathlib import Path

    ctx = browser.new_context()
    page = ctx.new_page()

    page.goto(f"{BASE}/register")
    page.fill("input[name=email]", EMAIL)
    page.fill("input[name=password]", PASSWORD)
    page.click("button:has-text('Register')")
    page.wait_for_load_state("networkidle")

    if "/profile" in page.url:
        page.fill("input[name=display_name]", "UI Tester")
        page.fill("input[name=title]", "Senior QA Engineer")
        page.fill("input[name=level]", "Senior")
        page.fill("input[name=company]", "Acme")
        page.fill("input[name=tech_context]", "Python API testing")
        page.click("button:has-text('Save profile')")
        page.wait_for_url(f"{BASE}/")

    ctx.close()
    yield EMAIL, PASSWORD

    # Teardown: remove the test users from the live DB so the next run starts fresh.
    db_path = Path(__file__).parent.parent.parent / "perfreviewbot.db"
    if db_path.exists():
        conn = sqlite3.connect(str(db_path))
        conn.execute("DELETE FROM assessment WHERE user_id IN "
                     "(SELECT id FROM user WHERE email IN (?, ?))",
                     (EMAIL, "ui_isolation@example.com"))
        conn.execute("DELETE FROM profile WHERE user_id IN "
                     "(SELECT id FROM user WHERE email IN (?, ?))",
                     (EMAIL, "ui_isolation@example.com"))
        conn.execute("DELETE FROM user WHERE email IN (?, ?)",
                     (EMAIL, "ui_isolation@example.com"))
        conn.commit()
        conn.close()


def _login(page, email: str = EMAIL, password: str = PASSWORD):
    """Log in and return when the home page is ready."""
    page.goto(f"{BASE}/login")
    page.fill("input[name=email]", email)
    page.fill("input[name=password]", password)
    page.click("button:has-text('Log in')")
    page.wait_for_url(f"{BASE}/")


def test_register_and_login(registered_user, page):
    """Log out then log back in — auth round-trip works."""
    _login(page)
    page.click("button:has-text('Log out')")
    page.wait_for_url(f"{BASE}/login")

    _login(page)
    assert "New assessment" in page.inner_text("body")


def test_assessment_renders_result(registered_user, page):
    """Submit a self-report and verify the verdict renders."""
    _login(page)
    page.fill("textarea[name=self_report]", "I write tests and report bugs.")
    page.click("button:has-text('Assess')")
    page.wait_for_selector("text=Overall verdict")

    text = page.inner_text("body")
    assert "Overall verdict" in text
    assert "Meets" in text
    assert "trending" in text.lower()


def test_result_shows_all_six_dimensions(registered_user, page):
    """Every scorecard dimension must appear in the rendered result."""
    _login(page)
    page.fill("textarea[name=self_report]", "I write tests and report bugs.")
    page.click("button:has-text('Assess')")
    page.wait_for_selector("text=Overall verdict")

    text = page.inner_text("body")
    for dim in [
        "Technical execution & automation",
        "Test strategy & quality ownership",
        "Autonomy & scope",
        "Influence & collaboration",
        "Mentorship",
        "Business & risk impact",
    ]:
        assert dim in text, f"Missing dimension: {dim}"


def test_history_records_assessment(registered_user, page):
    """After an assessment the history page shows a result."""
    _login(page)
    page.fill("textarea[name=self_report]", "I write tests and report bugs.")
    page.click("button:has-text('Assess')")
    page.wait_for_selector("text=Overall verdict")

    page.goto(f"{BASE}/history")
    text = page.inner_text("body")
    assert "Meets" in text
    assert "No assessments yet" not in text


def test_data_isolation_ui(registered_user, page, browser):
    """User B cannot see user A's history."""
    _login(page)
    page.fill("textarea[name=self_report]", "I write tests and report bugs.")
    page.click("button:has-text('Assess')")
    page.wait_for_selector("text=Overall verdict")

    # Fresh context = fresh session cookie → User B
    ctx_b = browser.new_context()
    page_b = ctx_b.new_page()
    page_b.goto(f"{BASE}/register")
    page_b.fill("input[name=email]", "ui_isolation@example.com")
    page_b.fill("input[name=password]", "pw2")
    page_b.click("button:has-text('Register')")
    page_b.wait_for_url(f"{BASE}/profile")
    page_b.fill("input[name=display_name]", "Other")
    page_b.click("button:has-text('Save profile')")
    page_b.wait_for_url(f"{BASE}/")

    page_b.goto(f"{BASE}/history")
    assert "No assessments yet" in page_b.inner_text("body")
    ctx_b.close()
