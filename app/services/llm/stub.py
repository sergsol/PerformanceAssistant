"""Deterministic stub LLM for unit/API/UI tests.

It encodes the project's core judgment in a crude but predictable way so tests
that mock the LLM stay fast and stable: if the self-report is only about writing
tests / reporting bugs, it returns Meets-trending-Below. This lets UI/API tests
assert on a stable result without hitting a real model. Real judgment quality is
tested separately in evals/ against a live model.
"""

from __future__ import annotations

import json
import re


def _dimension_names(user_prompt: str) -> list[str]:
    section = user_prompt.split("SCORECARD", 1)[-1].split("AGGREGATION GUIDANCE", 1)[0]
    return re.findall(r"^- (.+)$", section, flags=re.MULTILINE)


class StubClient:
    def complete_json(self, system: str, user: str, temperature: float = 0.2) -> str:
        # Inspect only the self-report section, not the scorecard template text
        # (which contains words like "strategy"/"mentor" in the dimension descriptions).
        marker = "WHAT THE PERSON DID THIS CYCLE"
        report_section = user.split(marker, 1)[1] if marker in user else user
        text = report_section.lower()
        execution_only = any(
            k in text for k in ["write test", "writing test", "report bug", "reporting bug"]
        )
        has_strategy = any(k in text for k in ["strategy", "own the", "prevent", "risk-based"])
        has_influence = any(
            k in text for k in ["mentor", "stakeholder", "present", "influence", "cross-team"]
        )

        def band(present: bool) -> str:
            return "Meets" if present else "Below"

        # Dimension names come from the SCORECARD section of the prompt so the stub
        # works for every role. Index convention (matches the original QA rubric):
        # 1 = strategy-like, 3 and 4 = influence/mentorship-like.
        names = _dimension_names(user)
        presence = {1: has_strategy, 3: has_influence, 4: has_influence}
        gaps = {
            1: "Own strategy for a feature.",
            3: "Present quality metrics to stakeholders.",
            4: "Mentor a junior tester.",
            0: "Improve the framework itself.",
        }
        dims = []
        for i, name in enumerate(names):
            b = band(presence[i]) if i in presence else "Meets"
            dims.append(
                {
                    "dimension": name,
                    "band": b,
                    "evidence": ["writes tests"] if i == 0 else [],
                    "gap": gaps.get(i) if (i in gaps and b != "Exceeds") else None,
                }
            )

        result = {
            "overall_band": "Meets",
            "overall_summary": "Stubbed assessment for testing.",
            "trending": "Below",
            "dimensions": dims,
            "recommendations": [
                "Own the test strategy for one feature end to end.",
                "Present quality metrics to stakeholders.",
            ],
        }
        # execution_only kept for readability of intent; result already reflects it.
        _ = execution_only
        return json.dumps(result)
