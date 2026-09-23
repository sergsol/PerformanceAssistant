from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.auth.jwt import decode_access_token
from app.db.models import User
from app.db.session import get_session

_bearer = HTTPBearer(auto_error=False)

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),  # noqa: B008
    session: Session = Depends(get_session),  # noqa: B008
) -> User | None:
    if credentials is None:
        return None
    try:
        user_id = decode_access_token(credentials.credentials)
    except ValueError:
        return None
    return session.get(User, user_id)

def require_user(user: User | None = Depends(get_current_user)) -> User:  # noqa: B008
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
