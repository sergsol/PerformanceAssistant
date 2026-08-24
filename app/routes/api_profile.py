from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from app.auth.deps import require_user
from app.db.models import Profile, User
from app.db.session import get_session

router = APIRouter(prefix="/api", tags=["profile"])

class ProfileOut(BaseModel):
    display_name: str
    title: str
    level: str
    scorecard_role: str
    company: str | None
    tech_context: str | None

class ProfileIn(BaseModel):
    display_name: str
    title: str = "Senior QA Engineer"
    level: str = "Senior"
    scorecard_role: str = "senior_qa"
    company: str | None = None
    tech_context: str | None = None

@router.get("/profile", response_model=ProfileOut)
def get_profile(user: User = Depends(require_user), session: Session = Depends(get_session)):
    profile = session.exec(select(Profile).where(Profile.user_id == user.id)).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileOut(**profile.model_dump())

@router.put("/profile", response_model=ProfileOut)
def update_profile(body: ProfileIn, user: User = Depends(require_user), session: Session = Depends(get_session)):
    profile = session.exec(select(Profile).where(Profile.user_id == user.id)).first()
    if not profile:
        profile = Profile(user_id=user.id, **body.model_dump())
        session.add(profile)
    else:
        for k, v in body.model_dump().items():
            setattr(profile, k, v)
    session.commit()
    session.refresh(profile)
    return ProfileOut(**profile.model_dump())
