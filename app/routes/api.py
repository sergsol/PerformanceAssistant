from __future__ import annotations

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlmodel import Session, select

from app.auth.deps import get_current_user
from app.db.models import Assessment, Profile, User
from app.db.session import get_session
from app.schemas.request import AssessRequest
from app.schemas.result import AssessResult
from app.scorecard.loader import load_scorecard
from app.services.assessor import assess
from app.services.llm import get_llm_client
from app.services.ratelimit import RateLimiter
from app.settings import get_settings

router = APIRouter(prefix="/api", tags=["assess"])


class AssessInput(BaseModel):
    """Anonymous assessment request: pick a role/level, describe your cycle."""

    self_report: str = Field(min_length=1)
    scorecard_role: str | None = Field(
        default=None,
        description="Scorecard key such as 'senior_qa' or 'mid_devops'. Defaults to the "
        "signed-in user's profile role if there is one, otherwise 'senior_qa'.",
    )
    company: str | None = Field(default=None, max_length=200)
    tech_context: str | None = Field(default=None, max_length=300)


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _check_rate_limit(request: Request) -> None:
    limiter: RateLimiter | None = getattr(request.app.state, "assess_limiter", None)
    if limiter is not None and not limiter.allow(_client_ip(request)):
        raise HTTPException(
            status_code=429, detail="Too many assessments from your network. Try again later."
        )


@router.post("/assess", response_model=AssessResult)
def api_assess(
    body: AssessInput,
    request: Request,
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """No account required. If a (legacy) signed-in user calls this, the result is
    also saved to their history, as before."""
    settings = get_settings()
    if len(body.self_report) > settings.assess_max_self_report_chars:
        raise HTTPException(
            status_code=422,
            detail="Self-assessment is too long "
            f"(max {settings.assess_max_self_report_chars} characters).",
        )
    _check_rate_limit(request)

    profile = None
    if user is not None:
        profile = session.exec(select(Profile).where(Profile.user_id == user.id)).first()
    role = body.scorecard_role or (profile.scorecard_role if profile else "senior_qa")
    try:
        card = load_scorecard(role)
    except KeyError:
        raise HTTPException(status_code=422, detail=f"Unknown role/level: {role!r}") from None

    req = AssessRequest(
        scorecard_role=role,
        title=card["role"],
        level=card["level"],
        company=body.company or (profile.company if profile else None),
        tech_context=body.tech_context or (profile.tech_context if profile else None),
        self_report=body.self_report,
    )
    client = get_llm_client()
    try:
        result = assess(req, client, role=role, temperature=settings.llm_temperature)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"LLM error {exc.response.status_code}: {exc.response.text[:300]}",
        ) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from None

    if user is not None:
        session.add(
            Assessment(
                user_id=user.id,
                self_report=body.self_report,
                result_json=result.model_dump_json(),
                overall_band=result.overall_band.value,
            )
        )
        session.commit()
    return result
