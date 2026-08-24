from __future__ import annotations
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.settings import get_settings

ALGORITHM = "HS256"
_EXPIRE_DAYS = 7

def create_access_token(user_id: int) -> str:
    s = get_settings()
    exp = datetime.now(timezone.utc) + timedelta(days=_EXPIRE_DAYS)
    return jwt.encode({"sub": str(user_id), "exp": exp}, s.secret_key, algorithm=ALGORITHM)

def decode_token(token: str) -> int:
    s = get_settings()
    try:
        payload = jwt.decode(token, s.secret_key, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise ValueError("missing sub")
        return int(sub)
    except JWTError as e:
        raise ValueError("invalid token") from e
