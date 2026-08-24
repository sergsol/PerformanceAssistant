from __future__ import annotations
from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from app.auth.deps import require_user
from app.db.models import Assessment, User
from app.db.session import get_session

router = APIRouter(prefix="/api", tags=["history"])

class HistoryItem(BaseModel):
    id: int
    created_at: datetime
    self_report: str
    overall_band: str
    result_json: str

@router.get("/history", response_model=list[HistoryItem])
def get_history(user: User = Depends(require_user), session: Session = Depends(get_session)):
    items = session.exec(
        select(Assessment)
        .where(Assessment.user_id == user.id)
        .order_by(Assessment.created_at.desc())
    ).all()
    return [HistoryItem(**item.model_dump()) for item in items]
