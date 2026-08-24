from __future__ import annotations
import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from app.auth.deps import require_user
from app.db.models import Assessment, Profile, User
from app.db.session import get_session
from app.schemas.result import AssessResult
from app.services.assessor import assess
from app.services.llm import get_llm_client
from app.settings import get_settings

router = APIRouter(prefix="/api", tags=["assess"])

class AssessInput(BaseModel):
    self_report: str = Field(min_length=1)

@router.post("/assess", response_model=AssessResult)
def api_assess(
    body: AssessInput,
    user: User = Depends(require_user),
    session: Session = Depends(get_session),
):
    profile = session.exec(select(Profile).where(Profile.user_id == user.id)).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Complete your profile before assessing")

    from app.schemas.request import AssessRequest
    req = AssessRequest(
        scorecard_role=profile.scorecard_role,
        title=profile.title,
        level=profile.level,
        company=profile.company,
        tech_context=profile.tech_context,
        self_report=body.self_report,
    )
    client = get_llm_client()
    try:
        result = assess(req, client, role=profile.scorecard_role,
                        temperature=get_settings().llm_temperature)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"LLM error {exc.response.status_code}: {exc.response.text[:300]}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    session.add(Assessment(
        user_id=user.id,
        self_report=body.self_report,
        result_json=result.model_dump_json(),
        overall_band=result.overall_band.value,
    ))
    session.commit()
    return result
