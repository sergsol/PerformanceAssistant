"""Authenticated web flow: new assessment (HTMX) + history.

The assess handler pulls the level from the stored profile, runs the assessor,
persists the assessment, and returns an HTML fragment for HTMX to swap in.
"""
from __future__ import annotations

import json

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.auth.deps import get_current_user, require_user
from app.db.models import Assessment, Profile, User
from app.db.session import get_session
from app.schemas.request import AssessRequest
from app.services.assessor import assess
from app.services.llm import get_llm_client
from app.settings import get_settings

router = APIRouter(tags=["web"])
templates = Jinja2Templates(directory="app/templates")

# Writing tips: activity → outcome. Grouped by role+level tier.
_TIPS: dict[str, list[dict]] = {
    "qa_early": [
        {"weak": "Reported bugs",
         "strong": "Filed 12 bug reports; 10 accepted as-is, 3 were critical severity that blocked release"},
        {"weak": "Ran test cases",
         "strong": "Executed the regression suite for checkout; caught a missed edge case on declined cards not in the test plan"},
        {"weak": "Attended meetings",
         "strong": "Asked clarifying questions in 3 sprint plannings that caught missing acceptance criteria before dev started"},
        {"weak": "Learned the automation framework",
         "strong": "Wrote 5 automated tests independently; my mentor reviewed them without major revisions"},
    ],
    "qa_mid": [
        {"weak": "Wrote test strategy",
         "strong": "Wrote the payments test strategy before dev started; 2 of 4 risk areas I flagged had zero coverage — I built tests for both"},
        {"weak": "Mentored junior QAs",
         "strong": "Mentored 2 junior QAs — they now independently write test strategies for small features and own their own PR reviews"},
        {"weak": "Improved the test suite",
         "strong": "Refactored the shared fixture library — cut the full regression suite from 18 min to 6 min, adopted by the whole team"},
        {"weak": "Collaborated with developers",
         "strong": "Flagged 3 quality risks in design reviews before any code was written; 2 were accepted and changed the implementation"},
    ],
    "qa_senior": [
        {"weak": "Owned test strategy",
         "strong": "Wrote and got sign-off on the test strategy before any code was written; identified 2 risk areas with zero existing coverage"},
        {"weak": "Mentored junior QAs",
         "strong": "Mentored 1 junior QA on property-based testing — they now own the fuzzing suite independently; it found 2 bugs in its first week"},
        {"weak": "Improved quality metrics",
         "strong": "Defect escape rate dropped 40% this cycle — directly attributable to the risk-based testing approach I introduced for the team"},
        {"weak": "Shared approach with other teams",
         "strong": "Presented the contract-testing pattern to 3 squads; 2 adopted it and caught breaking changes before staging"},
        {"weak": "Added AI to the pipeline",
         "strong": "Integrated AI-assisted failure analysis into CI — saved the team ~3 h/week; shared the setup guide with 2 other dev teams who adopted it"},
    ],
    "po_early": [
        {"weak": "Wrote requirements",
         "strong": "Ran 3 architect sessions to validate feasibility before writing specs; only 1 clarification needed during development"},
        {"weak": "Updated the roadmap",
         "strong": "Maintained the year-level roadmap and presented it to 2 enterprise customers; incorporated their feedback into Q4 prioritization"},
        {"weak": "Led product meetings",
         "strong": "Led 4 external customer calls and 8 internal planning sessions; resolved 3 competing stakeholder priorities with documented trade-offs"},
        {"weak": "Supported junior POs",
         "strong": "Paired with 2 junior POs on feature breakdown — after 3 sessions, they're writing acceptance criteria and breaking down stories independently"},
        {"weak": "Used AI for product work",
         "strong": "Built an AI agent to draft and validate requirements; reduced writing time ~50% and caught 4 inconsistencies before dev started"},
    ],
    "po_senior": [
        {"weak": "Worked on product strategy",
         "strong": "Defined the 18-month enterprise strategy; presented it to the CPO — it shaped 3 of the 5 company OKRs for the year"},
        {"weak": "Presented to customers",
         "strong": "Presented the year-level roadmap to 5 enterprise customers; 2 renewed based on roadmap commitments, 1 expanded scope"},
        {"weak": "Coordinated teams",
         "strong": "Resolved a 6-week dependency conflict between 3 teams by proposing a phased delivery model; all teams accepted, delivery stayed on track"},
        {"weak": "Mentored junior POs",
         "strong": "Mentored 3 POs — 1 was promoted to Senior; the other 2 now independently own their domain roadmaps and present to stakeholders"},
        {"weak": "Made data-driven decisions",
         "strong": "Defined 5 KPIs for the platform domain; all 5 are tracked in VP-level reporting and 3 improved quarter-over-quarter"},
    ],
    "dev_early": [
        {"weak": "Wrote code for the feature",
         "strong": "Implemented CSV export; reviewer said it was the cleanest code from a junior this quarter — merged with no major revisions"},
        {"weak": "Wrote tests",
         "strong": "Wrote unit tests covering 12 edge cases including nulls, unicode, and concurrent access — caught a race condition before review"},
        {"weak": "Helped team members",
         "strong": "Documented the async debugging approach I learned and posted it to the team wiki — 3 teammates referenced it the same week"},
        {"weak": "Fixed bugs",
         "strong": "Fixed 5 bugs; for the 2 most complex, I wrote a root-cause explanation in the PR so the team could avoid the pattern in future"},
    ],
    "dev_mid": [
        {"weak": "Designed the service",
         "strong": "Designed the token refresh flow, ran a review with 4 engineers, incorporated edge-case feedback — adopted as the team standard"},
        {"weak": "Mentored junior devs",
         "strong": "Mentored 2 junior devs through pairing and PR reviews — both shipped features independently this sprint that needed senior support last cycle"},
        {"weak": "Improved test coverage",
         "strong": "Introduced async testing patterns for our service layer; adopted by the team and found a race condition causing intermittent 500s for 6 weeks"},
        {"weak": "Worked with other teams",
         "strong": "Resolved an API contract conflict with 2 teams before dev started — saved an estimated 2 sprints of integration rework"},
    ],
    "dev_senior": [
        {"weak": "Designed the system",
         "strong": "Designed the service mesh migration for payments — adopted by 2 other domains; eliminated an entire class of timeout-related incidents"},
        {"weak": "Mentored engineers",
         "strong": "Formally mentored 3 engineers — 2 promoted to Senior this cycle; both are now independently leading multi-team technical projects"},
        {"weak": "Improved code quality",
         "strong": "Introduced the error handling standard company-wide — adopted across 8 services in 6 weeks; reduced error-related support tickets by 60%"},
        {"weak": "Fixed performance issues",
         "strong": "Reduced API p99 latency from 4 s to 280 ms — directly tied to a 12% improvement in checkout completion rate reported by product"},
        {"weak": "Shared at a conference",
         "strong": "Gave a talk on observable microservices at a regional conference; 2 companies adopted our approach based on the session"},
    ],
}

_TIPS_KEY: dict[str, str] = {
    "trainee_qa": "qa_early", "junior_qa": "qa_early",
    "mid_qa": "qa_mid",
    "senior_qa": "qa_senior", "staff_qa": "qa_senior", "principal_qa": "qa_senior",
    "associate_po": "po_early", "po": "po_early",
    "senior_po": "po_senior", "lead_po": "po_senior", "principal_po": "po_senior",
    "trainee_dev": "dev_early", "junior_dev": "dev_early",
    "mid_dev": "dev_mid",
    "senior_dev": "dev_senior", "staff_dev": "dev_senior", "principal_dev": "dev_senior",
}


@router.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if user is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    profile = session.exec(select(Profile).where(Profile.user_id == user.id)).first()
    if profile is None:
        return RedirectResponse(url="/profile", status_code=status.HTTP_303_SEE_OTHER)
    tips_key = _TIPS_KEY.get(profile.scorecard_role, "qa_senior")
    return templates.TemplateResponse(
        request, "index.html",
        {"profile": profile, "tips": _TIPS[tips_key]},
    )


@router.post("/assess", response_class=HTMLResponse)
def do_assess(
    request: Request,
    self_report: str = Form(...),
    user: User = Depends(require_user),
    session: Session = Depends(get_session),
):
    profile = session.exec(select(Profile).where(Profile.user_id == user.id)).first()
    req = AssessRequest(
        title=profile.title,
        level=profile.level,
        company=profile.company,
        tech_context=profile.tech_context,
        self_report=self_report,
    )
    client = get_llm_client()
    result = assess(req, client, role=profile.scorecard_role,
                    temperature=get_settings().llm_temperature)

    session.add(Assessment(
        user_id=user.id,
        self_report=self_report,
        result_json=result.model_dump_json(),
        overall_band=result.overall_band.value,
    ))
    session.commit()

    return templates.TemplateResponse(request, "_result.html", {"result": result})


@router.get("/history", response_class=HTMLResponse)
def history(
    request: Request,
    user: User = Depends(require_user),
    session: Session = Depends(get_session),
):
    rows = session.exec(
        select(Assessment).where(Assessment.user_id == user.id).order_by(Assessment.created_at.desc())
    ).all()
    items = [
        {"created_at": r.created_at, "overall_band": r.overall_band,
         "self_report": r.self_report, "result": json.loads(r.result_json)}
        for r in rows
    ]
    return templates.TemplateResponse(request, "history.html", {"items": items})
