"""Database models. Kept intentionally minimal.

Privacy note: Profile stores only role context the AI needs (title/level/company/
tech context) — no sensitive PII. This boundary is deliberate and is a QA/security
signal worth stating in the README.
"""
from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=_utcnow)

    profile: Optional["Profile"] = Relationship(back_populates="user")
    assessments: List["Assessment"] = Relationship(back_populates="user")


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True, unique=True)
    display_name: str
    title: str = "Senior QA Engineer"
    level: str = "Senior"
    company: Optional[str] = None
    tech_context: Optional[str] = None
    scorecard_role: str = "senior_qa"

    user: Optional[User] = Relationship(back_populates="profile")


class Assessment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    self_report: str
    result_json: str
    overall_band: str
    created_at: datetime = Field(default_factory=_utcnow)

    user: Optional[User] = Relationship(back_populates="assessments")
