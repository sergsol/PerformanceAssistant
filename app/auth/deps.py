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
    except IntegrityError:
        session.rollback()
        user = session.exec(select(User).where(User.session_id == session_id)).first()
        if user is None:
            raise
    return user


def get_current_user(request: Request, session: Session = Depends(get_session)) -> User | SimpleNamespace:
    """
    Extract user from JWT token in Authorization header: Bearer <token>
    Falls back to header-based identity (X-User-Id / X-User-Email) for backward compatibility.
    If no valid auth is found, returns an anonymous user object.
    """
    
    # Try JWT token first
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]  # Remove "Bearer " prefix
        try:
            user_id = decode_token(token)
            user = session.get(User, user_id)
            if user:
                return user
        except (ValueError, TypeError):
            pass  # Fall through to headers/anonymous
    
    # Try anonymous session header
    session_id = request.headers.get("X-Session-Id") or request.headers.get("X-User-Id")
    if session_id:
        return _get_or_create_anonymous_user(session_id, session)

    # Try numeric id header for backward compatibility
    user_id = request.headers.get("X-Db-User-Id")
    if user_id:
        try:
            user = session.get(User, int(user_id))
            if user:
                return user
        except (ValueError, TypeError):
            pass
    
    # Try email header
    user_email = request.headers.get("X-User-Email")
    if user_email:
        try:
            user = session.exec(select(User).where(User.email == user_email)).first()
            if user:
                return user
        except Exception:
            pass
    
    # Fallback anonymous user (has id and email attributes so routes expecting them won't crash)
    return SimpleNamespace(id=None, email=user_email or None)
    

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
