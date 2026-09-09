from __future__ import annotations
from fastapi import Depends, Request
from sqlmodel import Session, select
from types import SimpleNamespace

from app.db.session import get_session
from app.db.models import User


def get_current_user(request: Request, session: Session = Depends(get_session)) -> User | SimpleNamespace:
    """
    Legacy token auth removed. Support lightweight identity via headers:
      - X-User-Id: integer user id
      - X-User-Email: user's email

    If headers are provided, try to resolve a real User from DB.
    Otherwise return a simple anonymous object with id/email attributes so
    existing routes that expect them won't crash.
    """
    # Try numeric id header first
    user_id = request.headers.get("X-User-Id")
    if user_id:
        try:
            return session.get(User, int(user_id))
        except Exception:
            # ignore and fall through to anonymous
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
    return SimpleNamespace(id=None, email=user_email)
    

def require_user(user: User | SimpleNamespace = Depends(get_current_user)) -> User | SimpleNamespace:
    """
    Previously raised 401 if no authenticated user. Now always returns a user-like object
    (either a DB User or an anonymous object) so callers can continue to operate without auth.
    """
    return user
