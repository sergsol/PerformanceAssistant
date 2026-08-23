"""Unit tests for the pure assessor functions and scorecard loader (no network)."""
from __future__ import annotations

import json

import pytest

from app.scorecard.loader import dimension_names, load_scorecard
from app.schemas.request import AssessRequest
from app.schemas.result import AssessResult, Band
from app.services.assessor import build_prompt, parse_result


def test_scorecard_loads_six_dimensions():
    assert len(dimension_names("senior_qa")) == 6


def test_unknown_scorecard_raises():
    with pytest.raises(KeyError):
        load_scorecard("does_not_exist")


def test_build_prompt_includes_profile_and_scorecard():
    req = AssessRequest(title="Senior QA Engineer", level="Senior",
                        self_report="I write tests")
    system, user = build_prompt(req)
    assert "Senior" in user
    assert "Test strategy & quality ownership" in user
    assert "ONLY JSON" in system


def test_parse_result_strips_markdown_fences():
    payload = {
        "overall_band": "Meets", "overall_summary": "ok", "trending": "Below",
        "dimensions": [{"dimension": "X", "band": "Meets", "evidence": [], "gap": None}],
        "recommendations": [],
    }
    raw = "```json\n" + json.dumps(payload) + "\n```"
    result = parse_result(raw)
    assert isinstance(result, AssessResult)
    assert result.overall_band is Band.meets
    assert result.trending == "Below"


def test_parse_result_rejects_bad_band():
    bad = json.dumps({"overall_band": "Amazing", "overall_summary": "x",
                      "dimensions": [], "recommendations": []})
    with pytest.raises(Exception):
        parse_result(bad)
