"""JSON API. Clean boundary for API tests and programmatic use.

POST /api/assess accepts an AssessRequest and returns an AssessResult. It does
not require login (stateless), so schemathesis/httpx tests can hit it directly
with a stubbed LLM. The web flow (routes/web.py) is the authenticated path that
also persists history.
"""
from __future__ import annotations

import httpx
from fastapi import APIRouter, HTTPException

from app.schemas.request import AssessRequest
from app.schemas.result import AssessResult
from app.services.assessor import assess
from app.services.llm import get_llm_client
from app.settings import get_settings

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/assess", response_model=AssessResult)
def api_assess(req: AssessRequest) -> AssessResult:
    client = get_llm_client()
    try:
        return assess(req, client, role=req.scorecard_role,
                      temperature=get_settings().llm_temperature)
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"LLM API error: {exc.response.status_code} {exc.response.text[:300]}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
