"""Deterministic stub LLM for unit/API/UI tests.

It encodes the project's core judgment in a crude but predictable way so tests
that mock the LLM stay fast and stable: if the self-report is only about writing
tests / reporting bugs, it returns Meets-trending-Below. This lets UI/API tests
assert on a stable result without hitting a real model. Real judgment quality is
tested separately in evals/ against a live model.
"""
from __future__ import annotations

import json


class StubClient:
    def complete_json(self, system: str, user: str, temperature: float = 0.2) -> str:
        # Inspect only the self-report section, not the scorecard template text
        # (which contains words like "strategy"/"mentor" in the dimension descriptions).
        marker = "WHAT THE PERSON DID THIS CYCLE"
        report_section = user.split(marker, 1)[1] if marker in user else user
        text = report_section.lower()
        execution_only = any(k in text for k in ["write test", "writing test", "report bug", "reporting bug"])
        has_strategy = any(k in text for k in ["strategy", "own the", "prevent", "risk-based"])
        has_influence = any(k in text for k in ["mentor", "stakeholder", "present", "influence", "cross-team"])

        def band(present: bool) -> str:
            return "Meets" if present else "Below"

        result = {
            "overall_band": "Meets" if (has_strategy and has_influence) else "Meets",
            "overall_summary": "Stubbed assessment for testing.",
            "trending": None if (has_strategy and has_influence) else "Below",
            "dimensions": [
                {"dimension": "Technical execution & automation", "band": "Meets",
                 "evidence": ["writes tests"], "gap": "Improve the framework itself."},
                {"dimension": "Test strategy & quality ownership", "band": band(has_strategy),
                 "evidence": [], "gap": "Own strategy for a feature."},
                {"dimension": "Autonomy & scope", "band": "Meets", "evidence": [], "gap": None},
                {"dimension": "Influence & collaboration", "band": band(has_influence),
                 "evidence": [], "gap": "Present quality metrics to stakeholders."},
                {"dimension": "Mentorship", "band": band(has_influence),
                 "evidence": [], "gap": "Mentor a junior tester."},
                {"dimension": "Business & risk impact", "band": "Meets", "evidence": [], "gap": None},
            ],
            "recommendations": [
                "Own the test strategy for one feature end to end.",
                "Present quality metrics to stakeholders.",
            ],
        }
        # execution_only kept for readability of intent; result already reflects it.
        _ = execution_only
        return json.dumps(result)
