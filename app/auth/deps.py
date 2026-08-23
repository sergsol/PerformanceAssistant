"""Current-user dependencies.

`get_current_user` returns the logged-in User or None.
`require_user` raises 401 for API routes / redirects handled at route level.

Data isolation lives here in spirit: every route that touches user-owned data
must resolve the user via these deps and filter by user.id — never trust an id
from the request. The API tests assert user A cannot read user B's data.
"""
from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status
from sqlmodel import Session

from app.db.models import User
from app.db.session import get_session


def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
) -> User | None:
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return session.get(User, user_id)


def require_user(user: User | None = Depends(get_current_user)) -> User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login required",
        )
    return user
