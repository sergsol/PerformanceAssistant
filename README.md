# PerfReviewBot

An AI-powered self-assessment assistant for QA engineers. Store a profile (title, level, tech context), describe what you did this review cycle, and the assistant grades your work **Below / Meets / Exceeds** against a leveling rubric — per dimension and overall — then recommends how to move up a band.

> **This is a coaching / rehearsal tool, not an HR performance-review system.** It has no access to manager judgment, peer feedback, or company calibration. Treat it as a gap-check before your real review.

The real purpose of this repo is to be a **portfolio-grade demonstration of AI-native QA**: a real app (UI + API + a load-bearing AI feature) wrapped in a full, layered, CI-run test suite — including evals of the non-deterministic AI behavior itself.

![CI](https://github.com/sergsol/PerformanceAssistant/actions/workflows/ci.yml/badge.svg)

## The core idea it encodes

Writing tests and reporting bugs is solid *execution* — but for a Senior it's table-stakes. With test strategy, influence, mentorship, and business-impact empty, the verdict lands at **Meets — trending Below**, never Exceeds. The bot does not mistake *volume of low-level work* for seniority. That judgment is the whole point, and it's directly tested.

## What it does

**Flow:** `Register / Login` → `Profile setup` → `New assessment` → `Result` → `History`

- **Profile** (read by the AI): name, title/level, company, tech context. Kept minimal — no sensitive PII. This is the privacy boundary: the model sees role context, not personal data.
- **Assessment:** paste "what I did this cycle" — the AI already knows your level from the profile and grades against the right rubric.
- **Result:** per-dimension bands (6 dimensions) + overall verdict + evidence mapping + gaps + concrete recommendations.
- **History:** past assessments saved per user, viewable over time.

**The core judgment to get right** (and to test hardest): *"I write tests and report bugs"* is solid execution (Dimension 1) but is table-stakes for Senior. With Dimensions 2–6 empty, the overall verdict must land at **Meets-trending-Below**, NOT Meets or Exceeds. The model must not mistake volume of low-level work for seniority.

## The rubric

Synthesized from cross-company engineering/QA ladder patterns. Six dimensions for Senior QA:

| # | Dimension | One-line |
|---|-----------|----------|
| 1 | Technical execution & automation | Writes reliable tests/frameworks. **Caps at Meets alone.** |
| 2 | Test strategy & quality ownership | Owns strategy; shifts detection → prevention |
| 3 | Autonomy & scope | Self-directed on ambiguous quality problems |
| 4 | Influence & collaboration | Shapes how others test; stakeholder comms |
| 5 | Mentorship | Grows other testers |
| 6 | Business & risk impact | Ties quality to business outcomes; risk-based prioritization |

Also includes rubric levels for Junior/Mid/Staff/Principal QA, Trainee/Junior/Mid/Senior/Lead/Principal PO, and Trainee/Junior/Mid/Senior/Staff/Principal Dev. See [`app/scorecard/scorecard.yaml`](app/scorecard/scorecard.yaml).

## Architecture

```
Browser (HTMX + Alpine + Tailwind)
   │  POST /assess (form → HTML fragment)
   ▼
FastAPI
   ├─ routes/  auth · profile · web · api
   ├─ auth/    JWT + bcrypt
   ├─ db/      SQLModel: User · Profile · Assessment · RefreshToken
   ├─ scorecard/  scorecard.yaml (data) + loader
   ├─ schemas/ AssessRequest · AssessResult (the AI contract)
   └─ services/
        ├─ assessor.py       profile + scorecard + input → prompt → LLM → AssessResult
        └─ llm/              provider-agnostic: gemini · stub
   ▼
Gemini API (free tier)
```

Two assess endpoints on purpose: `POST /api/assess` returns JSON (for API tests and programmatic use); `POST /assess` returns an HTML fragment (the authenticated web flow that also persists history). Same `assessor` service underneath.

## Testing strategy (the point of the repo)

Five layers, all green in CI. This layered pyramid is the portfolio artifact.

| Layer | What | LLM |
|-------|------|-----|
| **Unit** | rubric loader, prompt builder, parser | none |
| **API** | functional, **auth**, **data-isolation**, persistence, schema validation | stubbed |
| **UI** | Playwright E2E: register → profile → assess → history | stubbed |
| **Evals** | band agreement vs golden dataset, **no grade inflation**, groundedness, schema validity | live |
| **Calibration** | stability across runs, monotonicity, level-sensitivity | live |

- Unit + API run on every PR (fast, deterministic).
- UI runs in its own CI stage (needs a running server + browser).
- Evals run on a schedule / on demand (they cost tokens and are rate-limited).

## Tech stack

Chosen so that (a) you stay in **one language (Python)** end to end, (b) the **testing story is maximal**, and (c) cost is **near zero**.

| Layer | Choice | Why |
|-------|--------|-----|
| Language | **Python 3.12** | One language across app + tests |
| Backend/API | **FastAPI** | Auto OpenAPI schema (feeds contract tests), async, industry-standard |
| Frontend | **React + Vite + TypeScript + Tailwind** | Modern, type-safe, test-friendly |
| Auth | **JWT (access + refresh tokens) + bcrypt** | Short-lived access tokens (15 min) + revocable refresh tokens (30 days) — real logout |
| Persistence | **SQLModel + SQLite/Postgres** | Swappable with one URL change |
| AI SDK | **Provider-agnostic wrapper** | Swap Gemini ↔ Groq via one interface |
| Primary AI | **Google Gemini Flash (free tier)** | Free, current-gen frontier models, no credit card |
| UI tests | **Playwright + pytest** | The headline UI automation skill |
| API tests | **pytest + httpx + schemathesis** | Schemathesis auto-generates tests from OpenAPI |
| AI evals | **promptfoo / DeepEval** | LLM-as-judge, golden datasets, thresholds in CI |
| CI | **GitHub Actions** | Runs all suites on PR; the green pyramid is the artifact |
| Deploy | **Render** (Docker) | Free tier, auto-deploy on push, live URL |
| Packaging | **uv + Dockerfile** | Reproducible env |

## Run locally

```bash
cp .env.example .env          # set SECRET_KEY; add GEMINI_API_KEY for real AI calls
pip install -e ".[dev]"
uvicorn app.main:app --reload   # http://localhost:8000
```

Use `LLM_PROVIDER=stub` to run the whole app with no API key (deterministic fake assessments — how the tests run).

## Test

```bash
# Fast suite — unit + API (no browser, no API key needed)
LLM_PROVIDER=stub pytest tests/unit tests/api -v

# UI suite — Playwright E2E (needs a running server + browser)
playwright install chromium
LLM_PROVIDER=stub uvicorn app.main:app --port 8000 &
pytest -m ui -v

# Evals — needs GEMINI_API_KEY (or GROQ_API_KEY)
pytest -m evals -v
```

## CI

GitHub Actions runs the full pyramid on every push and PR:

- **Lint** — ruff check
- **Unit + API** — `pytest` with `LLM_PROVIDER=stub` (fast, deterministic)
- **UI** — Playwright E2E against a running server (separate job with browser)
- **Evals** — runs on a weekly schedule + manual trigger (needs `GEMINI_API_KEY` secret, rate-limited)

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Deploy

Push the repo, then **Render → New + → Blueprint** and point it at this repo. `render.yaml` provisions a free web service (Docker) + free Postgres and wires `DATABASE_URL` automatically. Set `GEMINI_API_KEY` in the Render dashboard (not committed). On merge to `main`, Render auto-deploys.

Get a live URL → put it on your CV / LinkedIn / interview walkthrough.

Note: Render's free Postgres is deleted ~90 days after creation — fine for a demo.

## Privacy boundary

The profile stores only role context (title/level/company/tech context) — no sensitive personal data — because it's fed to the model. Scoping what the AI sees is a deliberate design choice, and it's something you can talk about in interviews.

## Project structure

```
perfreviewbot/
├── app/
│   ├── main.py              # FastAPI app + CORS
│   ├── settings.py          # pydantic-settings: DB URL, LLM keys, token TTLs
│   ├── auth/
│   │   ├── security.py      # bcrypt via passlib
│   │   ├── jwt.py           # access token creation/decode (short-lived JWT)
│   │   └── refresh.py       # refresh token: create/hash/verify/revoke (server-side)
│   ├── db/
│   │   ├── models.py        # User, Profile, Assessment, RefreshToken (SQLModel)
│   │   └── session.py       # engine + session factory
│   ├── scorecard/
│   │   ├── scorecard.yaml   # all role/level rubrics (data, not code)
│   │   └── loader.py        # loads + validates the scorecard
│   ├── schemas/
│   │   ├── request.py       # AssessRequest
│   │   └── result.py        # AssessResult, DimensionScore, Band enum
│   ├── services/
│   │   └── assessor.py      # prompt build → LLM → parse/validate → AssessResult
│   └── routes/
│       ├── api_auth.py      # register, login, refresh, revoke
│       ├── api_profile.py   # profile CRUD (JSON)
│       ├── api_history.py   # assessment history (JSON)
│       └── api.py           # POST /api/assess (JSON)
├── frontend/                # React + Vite + TypeScript + Tailwind
├── tests/
│   ├── unit/                # scorecard loader, prompt builder, parser
│   ├── api/                 # httpx functional + auth + data-isolation + schema
│   ├── ui/                  # Playwright E2E
│   └── conftest.py          # shared fixtures (stub LLM, fresh DB per test)
├── evals/                   # eval datasets + configs (run on schedule)
├── .github/workflows/ci.yml # CI: lint → unit/api → ui → evals (scheduled)
├── Dockerfile
├── render.yaml              # Render blueprint (web service + static frontend)
├── pyproject.toml
└── README.md
```

## Status

Phase 0–3 scaffolded: structure, auth (JWT + refresh tokens), DB, scorecard, schemas, Gemini client, assessor, web + API routes, templates, unit + API tests, Docker, CI, Render blueprint.

Next: Playwright E2E (Phase 6), golden dataset (Phase 7), evals (Phase 8).

See [PROJECT.md](PROJECT.md) for the full phased plan.

## What you can say in interviews

- "I built a full-stack AI app and tested it at five layers, all gated in CI."
- "For the non-deterministic AI feature I built evals: band-agreement against a golden dataset, an anti-inflation adversarial set, groundedness checks, and calibration/consistency tests."
- "I designed it provider-agnostic so I can swap Gemini and Groq and run evals across both."
- "I wrote the leveling rubric myself, grounded in industry ladder patterns — and encoded the judgment that execution volume isn't seniority."
- "My auth uses short-lived JWT access tokens (15 min) + revocable refresh tokens (30 days) with true server-side logout."

That last auth point is a real senior signal — most portfolio projects skip token hygiene.

## License

MIT
