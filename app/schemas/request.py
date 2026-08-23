"""Input contract for an assessment request."""
from __future__ import annotations

from pydantic import BaseModel, Field


class AssessRequest(BaseModel):
    # These come from the stored profile at assess time, but the API also
    # accepts them directly for programmatic use / testing.
    title: str = Field(examples=["Senior QA Engineer"])
    level: str = Field(examples=["Senior"])
    company: str | None = Field(default=None, examples=["Digital Turbine"])
    tech_context: str | None = Field(default=None, examples=["ad-tech / Creative Engine"])
    self_report: str = Field(
        min_length=1,
        description="What the person has been doing this cycle.",
        examples=["I write automated UI and API tests and report bugs."],
    )
