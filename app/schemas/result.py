"""The AI output contract. Every LLM response is parsed and validated into
AssessResult; anything that doesn't fit is a failure the tests will catch.
"""
from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class Band(str, Enum):
    below = "Below"
    meets = "Meets"
    exceeds = "Exceeds"


class DimensionScore(BaseModel):
    dimension: str = Field(description="Scorecard dimension name")
    band: Band
    evidence: list[str] = Field(
        default_factory=list,
        description="Quotes/paraphrases from the user's input that justify the band. "
        "Must be grounded in what the user actually wrote.",
    )
    gap: str | None = Field(
        default=None,
        description="What is missing to reach the next band, if not already Exceeds.",
    )


class AssessResult(BaseModel):
    overall_band: Band
    overall_summary: str = Field(description="1-3 sentence rationale for the overall verdict")
    trending: str | None = Field(
        default=None,
        description="Optional nuance, e.g. 'trending Below' when execution is strong "
        "but higher-order dimensions are empty.",
    )
    dimensions: list[DimensionScore]
    recommendations: list[str] = Field(
        default_factory=list,
        description="Concrete actions to move up a band.",
    )
