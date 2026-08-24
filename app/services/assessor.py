"""Assessor: the heart of the app.

profile + scorecard + self_report  ->  prompt  ->  LLM  ->  AssessResult

The prompt builder and parser are pure functions so they can be unit-tested
without any network (Phase 3 tests). The LLM call is injected via the LLMClient
interface so tests can pass a stub.
"""
from __future__ import annotations

import json
from typing import Any

from app.scorecard.loader import load_scorecard
from app.schemas.request import AssessRequest
from app.schemas.result import AssessResult
from app.services.llm.base import LLMClient

_SYSTEM = """You are a calibrated performance-review assistant.
You grade a person's self-reported work for one review cycle against a leveling
scorecard for their specific role and return a strict JSON verdict.

Rules you must follow:
- Grade against the role and level stated in the SCORECARD section. A Product Owner
  is graded on PO dimensions; a Developer on Developer dimensions; a QA Engineer on
  QA dimensions. Never apply a different role's expectations.
- Grade against the level in the PROFILE (e.g. Senior, Mid). Do NOT grade a Senior
  as if they were Mid or vice versa.
- Bands are RELATIVE TO THE LEVEL in the scorecard. The same body of work reads
  differently at different levels: what merely "Meets" for a Senior may clearly
  "Exceed" for a Mid or Junior, because the band descriptors themselves differ.
  If what the person wrote literally matches this scorecard's "Exceeds" descriptor
  for a dimension, score it "Exceeds" — do not withhold it because the work would
  be unremarkable at a higher level.
- Execution volume alone is NOT seniority. High output on tactical tasks that this
  scorecard's descriptors place at "Meets" must not be inflated to "Exceeds" by
  sheer quantity. This rule limits credit for VOLUME — it does not override a
  genuine descriptor match.
- Read the self-report semantically. Informal or casual writing still contains
  evidence. Phrase variety, typos, and brevity do not lower a score — only the
  absence of the underlying activity does.
- Every piece of evidence you cite MUST be grounded in what the user actually
  wrote. Do not invent achievements or penalise for things not mentioned.
- Do not inflate. Impressive-sounding but shallow work is still "Meets" at best.
- Return ONLY JSON matching the required schema. No prose, no markdown fences."""


def build_prompt(req: AssessRequest, role: str = "senior_qa") -> tuple[str, str]:
    """Return (system, user) prompt strings."""
    scorecard = load_scorecard(role)
    dims = "\n".join(
        f"- {d['name']}\n    Below: {d['below']}\n    Meets: {d['meets']}\n    Exceeds: {d['exceeds']}"
        for d in scorecard["dimensions"]
    )
    schema_hint = {
        "overall_band": "Below|Meets|Exceeds",
        "overall_summary": "string",
        "trending": "Below|null",
        "dimensions": [
            {"dimension": "string", "band": "Below|Meets|Exceeds",
             "evidence": ["string"], "gap": "string|null"}
        ],
        "recommendations": ["string"],
    }
    user = f"""PROFILE
  Title: {req.title}
  Level: {req.level}
  Company: {req.company or "n/a"}
  Tech context: {req.tech_context or "n/a"}

SCORECARD ({scorecard['role']} / {scorecard['level']})
{dims}

AGGREGATION GUIDANCE
{json.dumps(scorecard['aggregation'], indent=2)}

WHAT THE PERSON DID THIS CYCLE
{req.self_report}

Return JSON exactly matching this shape (one dimension object per scorecard dimension):
{json.dumps(schema_hint, indent=2)}

Gap rules (the "gap" field per dimension):
- For every dimension not at "Exceeds", state the SPECIFIC missing behavior, quoting the
  next band's expectation from the scorecard and contrasting it with what the person wrote.
- Phrase it as what is absent, e.g. "You describe writing tests, but nothing shows you
  choosing WHAT to test based on risk — that is the difference between Meets and Exceeds here."
- Never leave gap null for a "Below" or "Meets" dimension.

Recommendations rules:
- Include at least one recommendation for EVERY dimension that scored "Meets", stating
  the specific concrete action that would push it to "Exceeds" at this level.
- Include a recommendation for every dimension that scored "Below".
- Each recommendation must be a concrete action the person can start NEXT CYCLE, with a
  verifiable artifact or outcome (a document they write, a metric they move, a person they
  mentor, a meeting they run) — not an attitude change or generic advice.
- Where possible, build on something the person already does (e.g. "You already run the
  regression suite — next, write the risk-based test strategy for that area and get sign-off").
- Do not skip a dimension just because the person scored well overall."""
    return _SYSTEM, user


def parse_result(raw: str) -> AssessResult:
    """Parse and validate the model's JSON string into AssessResult.

    Strips accidental markdown fences defensively before parsing.
    """
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        # remove a leading 'json' language tag if present
        if cleaned.lstrip().lower().startswith("json"):
            cleaned = cleaned.lstrip()[4:]
    data: Any = json.loads(cleaned)
    return AssessResult.model_validate(data)


def assess(req: AssessRequest, client: LLMClient, role: str = "senior_qa",
           temperature: float = 0.2) -> AssessResult:
    system, user = build_prompt(req, role)
    raw = client.complete_json(system, user, temperature=temperature)
    return parse_result(raw)
