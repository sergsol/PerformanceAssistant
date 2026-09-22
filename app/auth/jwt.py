from __future__ import annotations
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.settings import Settings, get_settings

ALGORITHM = "HS256"


def _s() -> Settings:
    return get_settings()


def create_access_token(user_id: int) -> str:
    """Short-lived JWT access token (~15 min). Carries user_id, expires quickly."""
    s = _s()
    ttl = timedelta(minutes=s.access_token_ttl_minutes)
    exp = datetime.now(timezone.utc) + ttl
    return jwt.encode(
        {"sub": str(user_id), "exp": exp, "type": "access"},
        s.secret_key,
        algorithm=ALGORITHM,
    )


def create_refresh_token(user_id: int) -> str:
    """Opaque random refresh token. NOT a JWT — stored server-side, revocable.

    Returns the raw token string to be sent to the client (e.g. in a secure
    HTTP-only cookie or returned in the login response). The server stores
    a hash of it in the RefreshToken table.
    """
    import secrets
    return secrets.token_urlsafe(48)


def decode_access_token(token: str) -> int:
    """Decode a JWT access token. Returns user_id or raises ValueError."""
    s = _s()
    try:
        payload = jwt.decode(token, s.secret_key, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            raise ValueError("not an access token")
        sub = payload.get("sub")
        if sub is None:
            raise ValueError("missing sub")
        return int(sub)
    except JWTError as e:
        raise ValueError("invalid access token") from e


def access_token_expiry() -> datetime:
    """When the current access token expires (for the client to know when to refresh)."""
    s = _s()
    return datetime.now(timezone.utc) + timedelta(minutes=s.access_token_ttl_minutes)
