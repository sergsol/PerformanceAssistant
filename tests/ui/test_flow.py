"""End-to-end UI tests for the login-free flow (Python + Playwright + Pytest).

Flow under test: role selector -> self-assessment (with tips) -> performance result.
No account is created anywhere in these tests.

Run locally:
    cd frontend && npm ci && npm run build && cd ..
    LLM_PROVIDER=stub ASSESS_RATE_LIMIT_PER_HOUR=0 uvicorn app.main:app --port 8000 &
    playwright install chromium
    pytest -m ui
"""

from __future__ import annotations

import os
import re

import pytest
from playwright.sync_api import Page, expect

pytestmark = pytest.mark.ui

BASE = os.environ.get("BASE_URL", "http://localhost:8000")

ROLE_LABELS = [
    "Developer",
    "QA Engineer",
    "DevOps Engineer",
    "Security Specialist",
    "Product Owner",
    "Product Manager",
    "Project Manager",
    "HR / People",
]


def pick_role(page: Page, role_label: str, level_label: str) -> None:
    page.get_by_text(role_label, exact=True).first.click()
    page.select_option("select[name=level]", label=level_label)
    page.click("button:has-text('Continue')")


def submit_report(page: Page, text: str = "I write tests and report bugs.") -> None:
    page.fill("textarea[name=self_report]", text)
    page.click("button:has-text('Get assessment')")
    page.wait_for_selector("text=Overall verdict")


def test_first_page_is_role_selector_not_login(page: Page):
    page.goto(BASE)
    expect(page.get_by_role("heading", name=re.compile("performance", re.I))).to_be_visible()
    for label in ROLE_LABELS:
        expect(page.get_by_text(label, exact=True).first).to_be_visible()
    body = page.inner_text("body").lower()
    assert "log in" not in body
    assert "register" not in body
    assert page.locator("input[type=password]").count() == 0


@pytest.mark.parametrize("path", ["/login", "/register", "/profile", "/history"])
def test_legacy_account_urls_land_on_role_selector(page: Page, path: str):
    page.goto(f"{BASE}{path}")
    expect(page.get_by_text("1. Your role")).to_be_visible()


def test_deep_link_to_assess_without_choice_redirects_to_start(page: Page):
    page.goto(f"{BASE}/assess")
    expect(page.get_by_text("1. Your role")).to_be_visible()
    assert page.url.rstrip("/") == BASE.rstrip("/")


def test_level_requires_role_first(page: Page):
    page.goto(BASE)
    expect(page.locator("select[name=level]")).to_be_disabled()
    expect(page.get_by_role("button", name="Continue")).to_be_disabled()


def test_qa_flow_without_account_end_to_end(page: Page):
    page.goto(BASE)
    pick_role(page, "QA Engineer", "Senior QA Engineer")
    page.wait_for_url(f"{BASE}/assess")
    expect(page.get_by_text("Senior QA Engineer").first).to_be_visible()

    submit_report(page)
    text = page.inner_text("body")
    assert "Overall verdict" in text
    assert "trending" in text.lower()
    for dim in [
        "Technical execution & automation",
        "Test strategy & quality ownership",
        "Autonomy & scope",
        "Influence & collaboration",
        "Mentorship",
        "Business & risk impact",
    ]:
        assert dim in text, f"Missing dimension: {dim}"


NEW_ROLES = [
    ("Project Manager", "Senior Project Manager", "Risk & issue management"),
    ("Product Manager", "Senior Product Manager", "Discovery & customer insight"),
    ("DevOps Engineer", "Senior DevOps Engineer", "CI/CD & automation"),
    ("Security Specialist", "Senior Security Engineer", "Threat modeling & risk assessment"),
    ("HR / People", "Senior HR Business Partner", "People analytics & data"),
]


@pytest.mark.parametrize(("role", "level", "dimension"), NEW_ROLES)
def test_new_roles_assess_against_their_own_scorecard(
    page: Page, role: str, level: str, dimension: str
):
    page.goto(BASE)
    pick_role(page, role, level)
    page.wait_for_url(f"{BASE}/assess")
    submit_report(page, "I ran the main initiative this cycle.")
    assert dimension in page.inner_text("body")
    assert "Technical execution & automation" not in page.inner_text("body")


def test_tips_are_role_specific(page: Page):
    page.goto(BASE)
    pick_role(page, "Security Specialist", "Senior Security Engineer")
    page.click("text=Tips for a stronger self assessment")
    assert "threat model" in page.inner_text("body").lower()


def test_selection_survives_reload_and_can_be_changed(page: Page):
    page.goto(BASE)
    pick_role(page, "DevOps Engineer", "DevOps Engineer")
    page.wait_for_url(f"{BASE}/assess")
    page.reload()
    expect(page.get_by_test_id("current-role")).to_have_text("DevOps Engineer")

    page.click("text=Change role")
    page.wait_for_url(re.compile(re.escape(BASE) + r"/?$"))
    expect(page.locator("select[name=level]")).to_have_value("mid_devops")


def test_empty_self_assessment_cannot_be_submitted(page: Page):
    page.goto(BASE)
    pick_role(page, "Developer", "Senior Developer")
    page.wait_for_url(f"{BASE}/assess")
    expect(page.get_by_role("button", name="Get assessment")).to_be_disabled()
