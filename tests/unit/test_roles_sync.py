"""Guards: every role/level the UI offers has a scorecard, and every new role is well formed."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from app.scorecard.loader import _all_scorecards, load_scorecard

ROLES_TS = Path(__file__).parents[2] / "frontend" / "src" / "data" / "roles.ts"
NEW_FAMILIES = {
    "pm": ["junior_pm", "mid_pm", "senior_pm", "lead_pm"],
    "prodm": ["associate_prodm", "mid_prodm", "senior_prodm", "principal_prodm"],
    "devops": ["junior_devops", "mid_devops", "senior_devops", "staff_devops"],
    "security": ["junior_security", "mid_security", "senior_security", "staff_security"],
    "hr": ["associate_hr", "generalist_hr", "senior_hr", "lead_hr"],
}


def _ui_keys() -> list[str]:
    return re.findall(r"key: '([a-z_]+)'", ROLES_TS.read_text(encoding="utf-8"))


def test_every_ui_role_level_has_a_scorecard():
    keys = _ui_keys()
    assert len(keys) == 37
    missing = [k for k in keys if k not in _all_scorecards()]
    assert not missing, f"UI offers levels with no scorecard: {missing}"


def test_every_scorecard_is_offered_in_the_ui():
    unused = set(_all_scorecards()) - set(_ui_keys())
    assert not unused, f"Scorecards unreachable from the UI: {unused}"


@pytest.mark.parametrize("key", [k for keys in NEW_FAMILIES.values() for k in keys])
def test_new_role_scorecards_are_complete(key):
    card = load_scorecard(key)
    assert len(card["dimensions"]) == 6
    for dim in card["dimensions"]:
        assert dim["name"] and dim["below"] and dim["meets"] and dim["exceeds"]
    assert set(card["aggregation"]) >= {"exceeds", "meets", "below"}


@pytest.mark.parametrize("keys", NEW_FAMILIES.values())
def test_levels_differ_and_exceeds_points_up_the_ladder(keys):
    cards = [load_scorecard(k) for k in keys]
    for dim_idx in range(6):
        meets = [c["dimensions"][dim_idx]["meets"] for c in cards]
        assert len(set(meets)) == len(meets), "each level needs its own Meets expectation"
    # Exceeds at level N is the next level's Meets bar.
    first, second = cards[0], cards[1]
    assert second["dimensions"][0]["meets"] in first["dimensions"][0]["exceeds"]
