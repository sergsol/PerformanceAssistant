"""Database models. Kept intentionally minimal.

Privacy note: Profile stores only role context the AI needs (title/level/company/
tech context) — no sensitive PII. This boundary is deliberate and is a QA/security
signal worth stating in the README.
"""
from datetime import UTC, datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


def _utcnow() -> datetime:
    return datetime.now(UTC)


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=_utcnow)

    profile: Optional["Profile"] = Relationship(back_populates="user")
    assessments: list["Assessment"] = Relationship(back_populates="user")
    refresh_tokens: list["RefreshToken"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "delete"}
    )


class Profile(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True, unique=True)
    display_name: str
    title: str = "Senior QA Engineer"
    level: str = "Senior"
    company: str | None = None
    tech_context: str | None = None
    scorecard_role: str = "senior_qa"

    user: User | None = Relationship(back_populates="profile")


class Assessment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    self_report: str
    result_json: str
    overall_band: str
    created_at: datetime = Field(default_factory=_utcnow)

    user: User | None = Relationship(back_populates="assessments")


class RefreshToken(SQLModel, table=True):
    """Server-side refresh tokens. Enables true logout + token revocation.

    Each login/issue issues one refresh token. Revoking it invalidates the
    ability to get new access tokens — i.e. real logout from all devices
    that used that token.
    """
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    token_hash: str = Field(index=True, unique=True)  # hashed for storage
    expires_at: datetime
    revoked: bool = Field(default=False)
    created_at: datetime = Field(default_factory=_utcnow)

    user: User | None = Relationship(back_populates="refresh_tokens")
