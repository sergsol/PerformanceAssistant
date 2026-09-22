"""Refresh token handling: creation, hashing, verification, revocation."""

from __future__ import annotations
from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from app.db.models import RefreshToken
from app.db.session import engine
from app.settings import get_settings

import hashlib
import secrets
from typing import Optional


def _hash_token(raw: str) -> str:
    """SHA-256 hash of the raw refresh token for secure storage."""
    return hashlib.sha256(raw.encode()).hexdigest()


def create_refresh_token(user_id: int) -> str:
    """Generate a new refresh token for a user. Returns the raw token.

    The caller must store the hash in the RefreshToken table.
    """
    return secrets.token_urlsafe(48)


def store_refresh_token(user_id: int, raw_token: str) -> RefreshToken:
    """Hash and store a refresh token, returning the model."""
    ttl = get_settings().refresh_token_ttl_days
    with Session(engine) as session:
        rt = RefreshToken(
            user_id=user_id,
            token_hash=_hash_token(raw_token),
            expires_at=datetime.now(timezone.utc) + timedelta(days=ttl),
        )
        session.add(rt)
        session.commit()
        session.refresh(rt)
        return rt


def verify_refresh_token(raw_token: str) -> Optional[RefreshToken]:
    """Look up a refresh token by its hash. Returns the model or None."""
    hash_value = _hash_token(raw_token)
    with Session(engine) as session:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == hash_value)
        return session.exec(stmt).first()


def revoke_refresh_token(raw_token: str) -> bool:
    """Revoke a refresh token (logout). Returns True if it existed."""
    hash_value = _hash_token(raw_token)
    with Session(engine) as session:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == hash_value)
        rt = session.exec(stmt).first()
        if rt is None:
            return False
        rt.revoked = True
        session.add(rt)
        session.commit()
        return True


def revoke_all_user_tokens(user_id: int) -> int:
    """Revoke ALL refresh tokens for a user (e.g. password change)."""
    with Session(engine) as session:
        stmt = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False,
        )
        count = session.exec(stmt).unique().count()
        update_stmt = (
            RefreshToken.update()
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked == False,
            )
            .values({"revoked": True})
        )
        session.exec(update_stmt)
        session.commit()
        return count
