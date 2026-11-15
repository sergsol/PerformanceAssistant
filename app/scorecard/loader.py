"""Load scorecards from scorecard.yaml. Scorecards are data, not code, so new
roles/levels can be added without touching Python."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_SCORECARD_PATH = Path(__file__).parent / "scorecard.yaml"
_FAMILIES_PATH = Path(__file__).parent / "role_families.yaml"

_DEFAULT_AGGREGATION = {
    "exceeds": "Exceeds in >=3 dimensions with no dimension Below.",
    "meets": "Meets or better in >=4 dimensions.",
    "below": ">=3 dimensions Below.",
    "meets_trending_below": (
        "Meets overall, but strong gaps in the dimensions that matter most at this level."
    ),
}


def _expand_family(family: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Expand a compact role family (see role_families.yaml) into per-level scorecards.

    "Exceeds" for a level is the next level's "Meets" expectation (i.e. working at
    the next level's bar); the top level uses the dimension's explicit `top_exceeds`.
    """
    levels = family["levels"]
    out: dict[str, dict[str, Any]] = {}
    for idx, lvl in enumerate(levels):
        dims = []
        for dim in family["dimensions"]:
            if idx + 1 < len(levels):
                exceeds = (
                    f"Already operating at the {levels[idx + 1]['level']} bar: "
                    f"{dim['meets'][idx + 1]}"
                )
            else:
                exceeds = dim["top_exceeds"]
            dims.append(
                {
                    "name": dim["name"],
                    "below": dim["below"],
                    "meets": dim["meets"][idx],
                    "exceeds": exceeds,
                }
            )
        out[lvl["key"]] = {
            "role": lvl["role"],
            "level": lvl["level"],
            "dimensions": dims,
            "aggregation": dict(_DEFAULT_AGGREGATION),
        }
    return out


@lru_cache
def _all_scorecards() -> dict[str, Any]:
    with _SCORECARD_PATH.open("r", encoding="utf-8") as fh:
        cards: dict[str, Any] = yaml.safe_load(fh)
    with _FAMILIES_PATH.open("r", encoding="utf-8") as fh:
        families: dict[str, Any] = yaml.safe_load(fh)
    for family in families.values():
        cards.update(_expand_family(family))
    return cards


def load_scorecard(role: str = "senior_qa") -> dict[str, Any]:
    scorecards = _all_scorecards()
    if role not in scorecards:
        raise KeyError(f"Unknown scorecard role: {role!r}. Available: {list(scorecards)}")
    return scorecards[role]


def dimension_names(role: str = "senior_qa") -> list[str]:
    return [d["name"] for d in load_scorecard(role)["dimensions"]]
