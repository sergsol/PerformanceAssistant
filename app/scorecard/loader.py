"""Load scorecards from scorecard.yaml. Scorecards are data, not code, so new
roles/levels can be added without touching Python."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_SCORECARD_PATH = Path(__file__).parent / "scorecard.yaml"


@lru_cache
def _all_scorecards() -> dict[str, Any]:
    with _SCORECARD_PATH.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_scorecard(role: str = "senior_qa") -> dict[str, Any]:
    scorecards = _all_scorecards()
    if role not in scorecards:
        raise KeyError(f"Unknown scorecard role: {role!r}. Available: {list(scorecards)}")
    return scorecards[role]


def dimension_names(role: str = "senior_qa") -> list[str]:
    return [d["name"] for d in load_scorecard(role)["dimensions"]]
