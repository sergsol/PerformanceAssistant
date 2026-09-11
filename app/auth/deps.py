from __future__ import annotations
from fastapi import Depends, Request, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select
from types import SimpleNamespace

from app.db.session import get_session
from app.db.models import User
from app.auth.jwt import decode_token


def _get_or_create_anonymous_user(session_id: str, session: Session) -> User:
    user = session.exec(select(User).where(User.session_id == session_id)).first()
    if user:
        return user
    user = User(session_id=session_id)
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
        return user
    except IntegrityError:
        session.rollback()
        persisted_user = session.exec(select(User).where(User.session_id == session_id)).first()
        if persisted_user is None:
            raise
        return persisted_user


def get_current_user(request: Request, session: Session = Depends(get_session)) -> User | SimpleNamespace:
    """
    Resolve the current user from JWT auth, anonymous session headers, or legacy
    numeric/string user-id headers.

    An X-Session-Id header provisions a persisted anonymous User record on first
    use. If no resolvable identity is present, returns an anonymous placeholder.
    """

    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("******"):
        token = auth_header[7:]
        try:
            user_id = decode_token(token)
            user = session.get(User, user_id)
            if user:
                return user
        except (ValueError, TypeError):
            pass

    session_id = request.headers.get("X-Session-Id")
    if session_id:
        return _get_or_create_anonymous_user(session_id, session)

    user_id = request.headers.get("X-User-Id")
    if user_id:
        try:
            user = session.get(User, int(user_id))
            if user:
                return user
        except (ValueError, TypeError):
            if user_id.startswith("user_"):
                return _get_or_create_anonymous_user(user_id, session)

    return SimpleNamespace(id=None, email=None)


def require_user(user: User | SimpleNamespace = Depends(get_current_user)) -> User | SimpleNamespace:
    """
    Require an authenticated user. Raises 401 if no valid token or identity headers.
    """
    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
