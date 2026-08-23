# PerfReviewBot — Project Foundation

> An AI-powered self-assessment assistant that tells a QA engineer whether their
> current-cycle work reads as **Below / Meets / Exceeds** expectations for their
> level — grounded in a defined leveling rubric — and recommends what to do to
> move up a band.
>
> **This is a coaching / rehearsal tool, not an HR performance-review system.**
> It has no access to manager judgment, peer feedback, or company calibration.
> Framing it honestly as a "gap-check before your real review" is deliberate and
> is itself a point in its favor.

The real purpose of this repo is to be a **portfolio-grade demonstration of
AI-native QA**: a small but real app (UI + API + a load-bearing AI feature)
wrapped in a full, layered, CI-run automated test suite — including evals of the
non-deterministic AI behavior itself.

---

## 1. Why this project (the positioning angle)

An interviewer looking at this repo should immediately see three things:

1. **You can build and ship** a real full-stack app with a genuine AI feature.
2. **You can test all of it** — UI (Playwright), API (schema/contract), and the
   AI (evals, LLM-as-judge, calibration/consistency, anti-inflation).
3. **You have senior judgment** — you wrote a leveling rubric (a senior/staff
   activity), you scoped the tool honestly, and you know the difference between
   *execution* and *seniority* well enough to encode it.

The subject matter (what "Senior" means) reinforces the meta-message: you are
demonstrating the very seniority the tool measures.

---

## 2. What the app does

### Screens / flow (v1)
`Register / Login` → `Profile setup` → `New assessment` → `Result` → `History`

- **Profile** (read by the AI): name, title/level, company, project/tech context,
  tenure, applicable rubric role. **Kept minimal — no sensitive PII.** This is the
  privacy boundary: the model sees role context, not personal data.
- **New assessment:** user pastes only "what I did this cycle" — the AI already
  knows their level from the profile and grades against the right rubric.
- **Result:** per-dimension bands + overall verdict + evidence + gaps + recs.
- **History:** past assessments saved per user, viewable over time (trend toward
  Exceeds).

### Auth & data model
- Session-based login, bcrypt-hashed passwords.
- SQLite (SQLModel): `User`, `Profile`, `Assessment` (stores input + result JSON +
  timestamp).
- **Data isolation is a first-class test target:** user A must never read user B's
  profile or history.

**Inputs**
- Role + level (v1: hard-focus on **Senior QA**; from the stored profile;
  architecture allows other role/level rubrics later)
- A free-text description of what the user has been doing this cycle

**Outputs (structured JSON → rendered in UI)**
- A per-dimension band (**Below / Meets / Exceeds**) across 6 dimensions
- An overall band with rationale
- **Evidence mapping**: which of the user's statements satisfied which expectation
- **Gaps**: expectations with no supporting evidence
- **Recommendations**: concrete actions to reach the next band

**The core judgment to get right** (and to test hardest):
"I write tests and report bugs" is solid *execution* (Dimension 1) but is
table-stakes for Senior. With Dimensions 2–6 empty, the overall verdict must land
at **Meets-trending-Below**, NOT Meets or Exceeds. The model must not mistake
*volume of low-level work* for seniority.

---

## 3. The rubric (v1 — Senior QA)

Synthesized from common, cross-company engineering/QA ladder patterns (see
`RUBRIC.md` for the full Below/Meets/Exceeds descriptors and sources). Six
dimensions:

| # | Dimension | One-line |
|---|-----------|----------|
| 1 | Technical execution & automation | Writes reliable tests/frameworks. **Caps at Meets alone.** |
| 2 | Test strategy & quality ownership | Owns strategy; shifts detection → prevention |
| 3 | Autonomy & scope | Self-directed on ambiguous quality problems |
| 4 | Influence & collaboration | Shapes how others test; stakeholder comms |
| 5 | Mentorship | Grows other testers |
| 6 | Business & risk impact | Ties quality to business outcomes; risk-based prioritization |

The rubric IS the spec. Your golden-dataset labels are only meaningful relative
to it, so it is the real intellectual work of the project.

---

## 4. Tech stack

Chosen so that (a) you stay in **one language (Python)** end to end, (b) the
**testing story is maximal**, and (c) cost is **near zero**.

| Layer | Choice | Why |
|-------|--------|-----|
| Language | **Python 3.12** | You already know it; one language across app + tests |
| Backend/API | **FastAPI** | Auto OpenAPI schema (feeds schema/contract tests), async, industry-standard |
| Frontend | **Jinja2 + HTMX + Tailwind + Alpine.js** | Stay in Python; Tailwind for a modern look; Alpine for small client interactions (dropdowns/toggles). Playwright tests it identically. Keeps focus on testing, not JS tooling |
| Auth | **Session-based, passlib/bcrypt** | Lightweight but real; enables auth + data-isolation tests |
| Persistence | **SQLite + SQLModel** | Profiles + assessment history; a real data layer to test |
| AI SDK access | **Provider-agnostic wrapper** | Swap Gemini ↔ Groq via one interface (a good design signal) |
| Primary AI model | **Google Gemini Flash (free tier)** | Only free tier with current frontier models, no credit card, multimodal, generous cap |
| Alt AI model | **Groq (Llama, free tier)** | 30 req/min, very fast, open-source models; good for CI eval runs |
| Structured output | Pydantic models + JSON mode | Enforce/validate the response schema |
| UI tests | **Playwright + pytest** | The headline UI automation skill |
| API tests | **pytest + httpx + schemathesis** | schemathesis auto-generates tests from OpenAPI — strong to show |
| AI evals | **promptfoo** and/or **DeepEval** | LLM-as-judge, golden datasets, thresholds in CI |
| CI | **GitHub Actions** | Runs all suites on PR; the green pyramid is the artifact |
| Deployment | **Render** (backend) or single **Docker** image; **Fly.io** as alt | Free/cheap tiers; Docker keeps it portable |
| Packaging | **uv** or poetry + Dockerfile | Reproducible env |
| Config | pydantic-settings + `.env` | API keys never in code |

### On the AI model choice (verified current as of Aug 2026)
- **Free tiers with current frontier models:** Google Gemini API — Flash-family
  models are free, no credit card, only free tier that includes
  current-generation frontier models.
- **Groq** free tier: 30 requests/min, fast inference, open-source models only
  (Llama/Qwen/etc.). Great for high-volume eval runs.
- Both are enough for this project. Building against a **provider-agnostic
  interface** means you can demo model-swapping and run evals across providers —
  a sophisticated thing to show. Never hard-code one vendor.

---

## 5. Architecture

```
┌──────────────────────────────────────────────────────────┐
│  Browser (HTMX)                                           │
│  - form: level + "what I've been doing"                  │
│  - renders returned HTML fragment (bands, gaps, recs)    │
└───────────────┬──────────────────────────────────────────┘
                │  POST /assess  (form → HTML fragment)
                ▼
┌──────────────────────────────────────────────────────────┐
│  FastAPI app                                             │
│  ├─ routes/          (web + JSON API endpoints)          │
│  ├─ schemas/         (Pydantic: request + AssessResult)  │
│  ├─ rubric/          (rubric.yaml + loader)              │
│  ├─ services/                                           │
│  │   ├─ assessor.py  (prompt build → LLM → parse/validate)│
│  │   └─ llm/         (provider-agnostic client)         │
│  │        ├─ base.py     (LLMClient protocol)           │
│  │        ├─ gemini.py                                  │
│  │        └─ groq.py                                    │
│  └─ templates/       (Jinja2 + HTMX)                     │
└───────────────┬──────────────────────────────────────────┘
                │
                ▼
        External LLM API (Gemini / Groq)
```

Two endpoints on purpose:
- `POST /assess` → returns an **HTML fragment** (HTMX, for the UI)
- `POST /api/assess` → returns **JSON** (for API tests + programmatic use)

Both call the same `assessor` service. This separation means your API tests hit
clean JSON while your UI tests drive the rendered page — and it demonstrates you
understand the value of a testable API boundary.

---

## 6. Repository structure

```
perfreviewbot/
├── app/
│   ├── main.py
│   ├── routes/
│   │   ├── auth.py           # register, login, logout (sessions)
│   │   ├── profile.py        # profile CRUD (web + JSON)
│   │   ├── web.py            # GET /, POST /assess (HTML), history views
│   │   └── api.py            # POST /api/assess, /api/profile (JSON)
│   ├── db/
│   │   ├── models.py         # User, Profile, Assessment (SQLModel)
│   │   └── session.py
│   ├── auth/
│   │   ├── security.py       # bcrypt hashing, session helpers
│   │   └── deps.py           # current-user dependency
│   ├── schemas/
│   │   ├── request.py        # AssessRequest
│   │   └── result.py         # AssessResult, DimensionScore, Band(enum)
│   ├── rubric/
│   │   ├── rubric.yaml       # the Senior QA rubric (data, not code)
│   │   └── loader.py
│   ├── services/
│   │   ├── assessor.py
│   │   └── llm/
│   │       ├── base.py
│   │       ├── gemini.py
│   │       └── groq.py
│   ├── templates/
│   │   ├── base.html         # Tailwind layout, Alpine loaded
│   │   ├── login.html / register.html
│   │   ├── profile.html      # profile setup/edit
│   │   ├── index.html        # new assessment
│   │   ├── history.html      # past assessments
│   │   └── _result.html      # HTMX fragment
│   └── settings.py
├── tests/
│   ├── unit/                 # rubric loader, prompt builder, parsers
│   ├── api/                  # httpx + schemathesis
│   ├── ui/                   # Playwright
│   └── conftest.py
├── evals/
│   ├── datasets/
│   │   ├── golden.jsonl      # (level, self_report) → expected bands + gaps
│   │   └── adversarial.jsonl # impressive-sounding but only-Meets inputs
│   ├── promptfooconfig.yaml
│   ├── deepeval_tests.py
│   └── metrics/              # custom: no-inflation, monotonicity, calibration
├── .github/workflows/
│   └── ci.yml                # unit → api → ui → evals
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── .env.example
└── README.md
```

---

## 7. Testing strategy (the whole point)

Five layers, all green in CI. This layered pyramid is the portfolio artifact.

### L1 — Unit (fast, deterministic)
Rubric loader, prompt builder, response parser/validator. No network.

### L2 — API functional + schema
- Functional: `httpx` against the JSON endpoint (happy path, bad input, empty
  input, oversized input).
- **Auth tests:** login required on protected routes, wrong password rejected,
  session expiry, logout.
- **Authorization / data-isolation tests (senior signal):** user A cannot read or
  mutate user B's profile or assessment history. This is often the most impressive
  test in the suite.
- **Persistence tests:** profile save/load, assessment history integrity,
  constraints.
- **Schema/fuzz: `schemathesis`** auto-derives cases from the OpenAPI spec — one
  config, broad coverage. Very strong to show.
- The LLM is **mocked/stubbed** here so these tests are deterministic and fast.

### L3 — UI E2E (Playwright)
User fills the form, submits, sees bands + gaps + recs rendered. Covers the
HTMX swap. LLM stubbed via a test flag or a fake provider for determinism.

### L4 — AI evals (the differentiator)
Run against a **golden dataset** with real model calls (throttled to free-tier
limits; can target Groq for speed). Metrics:
1. **Band agreement** — model band vs human-labeled band per dimension
   (exact + within-one-band tolerance). LLM-as-judge for rationale quality.
2. **No grade inflation** — adversarial set of impressive-sounding-but-Meets
   inputs; assert the model does NOT return Exceeds. (Precision on "Exceeds".)
3. **Groundedness** — every evidence-mapping claim must trace to something the
   user actually wrote (no fabricated evidence).
4. **Structured-output validity** — 100% of responses parse against the Pydantic
   schema.

### L5 — Calibration / consistency (non-determinism handling)
1. **Stability** — same input N times → band stable (majority vote + variance
   under threshold).
2. **Monotonicity** — strictly more/stronger evidence must never lower a band.
3. **Level sensitivity** — same self-report at Mid vs Senior vs Staff yields
   appropriately different verdicts (parametrized).

> Threshold gates: evals fail CI if band-agreement < X% or any inflation case
> returns Exceeds. Pick conservative thresholds and tighten over time.

---

## 8. Deployment

**Goal: free/cheap, reproducible, demonstrable.**

- **Local:** `docker compose up` → app on `localhost:8000`.
- **Hosted (pick one):**
  - **Render** — free web-service tier, connects to GitHub, auto-deploy on push.
  - **Fly.io** — free allowance, deploys the Docker image, good for a global URL.
  - Either gives you a **live URL to put on your CV / LinkedIn**.
- **Secrets:** API keys as environment variables in the host's dashboard; never
  committed. `.env.example` documents required vars.
- **CI/CD:** GitHub Actions runs the full test pyramid on every PR; on merge to
  `main`, the host auto-deploys. Showing green CI → auto-deploy is itself a
  senior signal (you own the pipeline, not just the tests).

---

## 9. Roadmap (phased — each phase is shippable & interview-talkable)

**Phase 0 — Skeleton (½–1 day)**
Repo, pyproject, FastAPI hello, Dockerfile, GitHub Actions running an empty
pytest. Deploy the skeleton to Render → live URL from day one.

**Phase 1 — Data model + auth (1–2 days)**
SQLModel `User`/`Profile`/`Assessment`. Session-based register/login/logout with
bcrypt. Current-user dependency. Unit-test security helpers.

**Phase 2 — Rubric + schema (1 day)**
Write `rubric.yaml` (all 6 dims × 3 bands). Define Pydantic `AssessRequest` /
`AssessResult`. Unit-test the loader + schema. *No AI yet.*

**Phase 3 — LLM integration (1–2 days)**
Provider-agnostic client (Gemini first, Groq second). `assessor.py`: build
prompt from **profile + rubric + input** → call model → parse/validate to
`AssessResult`. JSON endpoints `POST /api/assess`, profile CRUD. Persist
assessments. Unit-test prompt builder + parser with a stub.

**Phase 4 — API tests (1–2 days)**
httpx functional + **auth + data-isolation + persistence** tests + schemathesis
against OpenAPI. LLM mocked. Wire into CI.

**Phase 5 — UI (2 days)**
Tailwind base layout; login/register, profile, new-assessment, result fragment,
history screens. HTMX for the assess swap; Alpine for small interactions.

**Phase 6 — UI tests (1 day)**
Playwright E2E: register → set profile → assess → see result → view history, with
stubbed LLM. Wire into CI. (Now: 3 green suites.)

**Phase 7 — Golden dataset (1–2 days)**
Hand-label 20–40 (level, self_report) → expected bands + gaps. Include YOUR own
"just tests + bugs" case as a labeled example. Add the adversarial set.

**Phase 8 — Evals (2–3 days)**
promptfoo/DeepEval: band agreement, no-inflation, groundedness, schema validity.
Add calibration/consistency + monotonicity + level-sensitivity. Threshold gates
in CI (may run on a schedule / separate job due to rate limits & API cost).

**Phase 9 — Polish & positioning (1 day)**
README with the test-pyramid diagram + live demo link + eval results badge.
Write the LinkedIn post. Prep the interview walkthrough narrative.

> Realistic total: ~3–4 focused weeks part-time (auth + history add ~a week).
> Every phase leaves `main` green and deployable, so you can start talking about
> it in interviews after Phase 4 (auth + data-isolation tests are a strong story
> on their own).

---

## 10. What you'll be able to say in interviews

- "I built a full-stack AI app and tested it at five layers, all gated in CI."
- "For the non-deterministic AI feature I built evals: band-agreement against a
  golden dataset, an anti-inflation adversarial set, groundedness checks, and
  calibration/consistency tests for the non-determinism."
- "I designed it provider-agnostic so I can swap Gemini and Groq and run evals
  across both."
- "I wrote the leveling rubric myself, grounded in industry ladder patterns —
  and encoded the judgment that execution volume isn't seniority."

That last one is the whole game: it shows you know what Senior *means*.

---

## 11. Open decisions to confirm next
1. Confirm the 6 rubric dimensions (or adjust) — see `RUBRIC.md`.
2. Primary model: start on **Gemini Flash free** (recommended) or Groq?
3. Deploy target: **Render** (simplest) or Fly.io?
4. Eval framework: **promptfoo** (config-driven, easy) vs **DeepEval**
   (pytest-native) — or both. Recommend starting with promptfoo.
