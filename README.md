# PerfReviewBot

An AI-powered self-assessment assistant for QA engineers. You store a profile
(title, level, tech context), describe what you did this review cycle, and the
assistant grades your work **Below / Meets / Exceeds** against a leveling rubric —
per dimension and overall — then recommends how to move up a band.

> **This is a coaching / rehearsal tool, not an HR performance-review system.** It
> has no access to manager judgment, peer feedback, or company calibration. Treat
> it as a gap-check before your real review.

The real purpose of this repo is to be a **portfolio-grade demonstration of
AI-native QA**: a real app (UI + API + a load-bearing AI feature) wrapped in a
full, layered, CI-run test suite — including evals of the non-deterministic AI
behaviour itself.

## The core idea it encodes

Writing tests and reporting bugs is solid *execution* — but for a Senior it's
table-stakes. With test strategy, influence, mentorship, and business-impact
empty, the verdict lands at **Meets — trending Below**, never Exceeds. The bot
does not mistake *volume of low-level work* for seniority. That judgment is the
whole point, and it's directly tested.

## Stack

- **Backend/API:** FastAPI (Python) — auto OpenAPI schema feeds the API tests
- **Frontend:** Jinja2 + HTMX + Tailwind + Alpine.js (modern look, stays in Python)
- **Auth:** session cookies + bcrypt
- **DB:** SQLModel — **SQLite** locally & in tests, **Postgres** in production (one URL change)
- **AI:** provider-agnostic wrapper; **Google Gemini Flash** (free tier) primary, Groq planned, stub for tests
- **Tests:** pytest, Playwright, schemathesis, DeepEval + promptfoo (evals)
- **CI/CD:** GitHub Actions → auto-deploy on Render

## Architecture

```
Browser (HTMX + Alpine + Tailwind)
   │  POST /assess (form → HTML fragment)
   ▼
FastAPI
   ├─ routes/  auth · profile · web · api
   ├─ auth/    bcrypt + session dep (enforces data isolation)
   ├─ db/      SQLModel: User · Profile · Assessment
   ├─ rubric/  rubric.yaml (data) + loader
   ├─ schemas/ AssessRequest · AssessResult (the AI contract)
   └─ services/
        ├─ assessor.py       profile + rubric + input → prompt → LLM → AssessResult
        └─ llm/              provider-agnostic: gemini · (groq) · stub
   ▼
Gemini API (free tier)
```

Two assess endpoints on purpose: `POST /api/assess` returns JSON (for API tests
and programmatic use); `POST /assess` returns an HTML fragment (the authenticated
web flow that also persists history). Same `assessor` service underneath.

## Testing strategy (the point of the repo)

| Layer | What | LLM |
|-------|------|-----|
| Unit | rubric loader, prompt builder, parser | none |
| API | functional, **auth**, **data-isolation**, persistence, schemathesis fuzz | stubbed |
| UI | Playwright E2E: register → profile → assess → history | stubbed |
| Evals | band agreement vs golden dataset, **no grade inflation**, groundedness, schema validity | live |
| Calibration | stability across runs, monotonicity, level-sensitivity | live |

Unit + API run on every PR (fast, deterministic). UI runs in its own CI stage.
Evals run on demand / schedule (they cost tokens and are rate-limited).

## Run locally

```bash
cp .env.example .env          # set SECRET_KEY; add GEMINI_API_KEY for real calls
pip install ".[dev]"
uvicorn app.main:app --reload # http://localhost:8000
```

Use `LLM_PROVIDER=stub` to run the whole app with no API key (deterministic
fake assessments — how the tests run).

## Test

```bash
LLM_PROVIDER=stub pytest tests/unit tests/api -v   # fast suite
playwright install chromium && pytest -m ui        # UI (needs running server)
pytest -m evals                                     # evals (needs GEMINI_API_KEY)
```

## Deploy (Render)

Push the repo, then **New + → Blueprint** and point it at this repo. `render.yaml`
provisions a free web service + free Postgres and wires `DATABASE_URL`
automatically. Set `GEMINI_API_KEY` in the dashboard (not committed). On merge to
`main`, Render auto-deploys.

Note: Render's free Postgres is deleted ~90 days after creation — fine for a demo.

## Privacy boundary

The profile stores only role context (title/level/company/tech context) — no
sensitive personal data — because it's fed to the model. Scoping what the AI sees
is a deliberate design choice.

## Status / roadmap

Phase 0–3 scaffolded (structure, auth, DB, rubric, schemas, Gemini client,
assessor, web+API routes, templates, unit+API tests, Docker, CI, Render blueprint).
Next: flesh out Playwright E2E (Phase 6), golden dataset (Phase 7), evals (Phase 8).
See `PROJECT.md` for the full phased plan.
