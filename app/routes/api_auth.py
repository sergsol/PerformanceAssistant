from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from app.auth.jwt import create_access_token
from app.auth.refresh import (
    create_refresh_token as make_refresh,
)
from app.auth.refresh import (
    revoke_refresh_token,
    store_refresh_token,
    verify_refresh_token,
)
from app.auth.security import hash_password, verify_password
from app.db.models import User
from app.db.session import get_session
from app.settings import get_settings

router = APIRouter(prefix="/api/auth", tags=["auth"])

_bearer = HTTPBearer()


# ── Request/Response models ──────────────────────────────────────────

class AuthRequest(BaseModel):
    email: str = Field(min_length=1, max_length=254)
    password: str = Field(min_length=8)


class TokenPairResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int                    # seconds until access token expires
    refresh_token: str                # opaque, store client-side for refresh


class RefreshRequest(BaseModel):
    refresh_token: str


# ── Auth endpoints ───────────────────────────────────────────────────

@router.post("/register", response_model=TokenPairResponse, status_code=201)
def register(body: AuthRequest, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.email == body.email)).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(email=body.email, password_hash=hash_password(body.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    uid = user.id
    assert uid is not None

    raw_refresh = make_refresh(uid)
    store_refresh_token(uid, raw_refresh)   # commits internally

    access = create_access_token(uid)
    return TokenPairResponse(
        access_token=access,
        expires_in=60 * get_settings().access_token_ttl_minutes,
        refresh_token=raw_refresh,
    )


@router.post("/login", response_model=TokenPairResponse)
def login(body: AuthRequest, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == body.email)).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    uid = user.id
    assert uid is not None

    raw_refresh = make_refresh(uid)
    store_refresh_token(uid, raw_refresh)   # commits internally

    access = create_access_token(uid)
    return TokenPairResponse(
        access_token=access,
        expires_in=60 * get_settings().access_token_ttl_minutes,
        refresh_token=raw_refresh,
    )


@router.post("/refresh", response_model=TokenPairResponse)
def refresh(body: RefreshRequest):
    """Swap a valid refresh token for a new access token (+ new refresh token).

    Refresh tokens are single-use: using one revokes it and issues a new one.
    This limits the window of exposure if a refresh token is leaked.
    """
    rt = verify_refresh_token(body.refresh_token)
    if rt is None or rt.revoked or rt.expires_at <= datetime.now(UTC):
        raise HTTPException(status_code=401, detail="Refresh token invalid or expired")

    uid = rt.user_id
    # Revoke the old token
    revoke_refresh_token(body.refresh_token)

    new_refresh = make_refresh(uid)
    store_refresh_token(uid, new_refresh)   # commits internally

    access = create_access_token(uid)
    return TokenPairResponse(
        access_token=access,
        expires_in=60 * get_settings().access_token_ttl_minutes,
        refresh_token=new_refresh,
    )


@router.post("/revoke", status_code=204)
def revoke(body: RefreshRequest):
    """Revoke a refresh token — server-side logout."""
    if not revoke_refresh_token(body.refresh_token):
        raise HTTPException(status_code=404, detail="Refresh token not found")
