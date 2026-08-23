"""Profile CRUD. All operations are scoped to the current user — the user id is
taken from the session, never from the request body, which is what enforces data
isolation."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlmodel import Session, select

from app.auth.deps import require_user
from app.db.models import Profile, User
from app.db.session import get_session

router = APIRouter(tags=["profile"])
templates = Jinja2Templates(directory="app/templates")


def _get_or_none(session: Session, user_id: int) -> Profile | None:
    return session.exec(select(Profile).where(Profile.user_id == user_id)).first()


@router.get("/profile", response_class=HTMLResponse)
def profile_form(
    request: Request,
    user: User = Depends(require_user),
    session: Session = Depends(get_session),
):
    profile = _get_or_none(session, user.id)
    return templates.TemplateResponse(request, "profile.html", {"profile": profile})


@router.post("/profile")
def save_profile(
    request: Request,
    display_name: str = Form(...),
    title: str = Form("Senior QA Engineer"),
    level: str = Form("Senior"),
    scorecard_role: str = Form("senior_qa"),
    company: str = Form(""),
    tech_context: str = Form(""),
    user: User = Depends(require_user),
    session: Session = Depends(get_session),
):
    profile = _get_or_none(session, user.id)
    if profile is None:
        profile = Profile(user_id=user.id, display_name=display_name)
    profile.display_name = display_name
    profile.title = title
    profile.level = level
    profile.scorecard_role = scorecard_role
    profile.company = company or None
    profile.tech_context = tech_context or None
    session.add(profile)
    session.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
