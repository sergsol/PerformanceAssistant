#!/usr/bin/env bash
# Run this once in your terminal to create all epics and stories on GitHub.
# Prerequisites: gh CLI installed and authenticated (gh auth login)
# Usage: bash docs/create_github_issues.sh

REPO="sergsol/PerformanceAssistant"

echo "Creating labels..."
gh label create "epic" --color "0075ca" --description "Epic — top-level feature group" --repo $REPO 2>/dev/null || true
gh label create "story" --color "e4e669" --description "User story" --repo $REPO 2>/dev/null || true
gh label create "learning" --color "d93f0b" --description "Has learning resources attached" --repo $REPO 2>/dev/null || true

echo ""
echo "=== EPIC 1: Project Setup & Infrastructure ==="
E1=$(gh issue create --repo $REPO \
  --title "Epic 1: Project Setup & Infrastructure" \
  --label "epic" \
  --body "Set up the project skeleton, tooling, and development environment from scratch.

## Outcome
A developer can clone the repo, run one command, and have a working local environment.

## Stories
- [ ] Initialize Git repo with .gitignore and pyproject.toml
- [ ] Set up Python virtual environment and dependencies
- [ ] Configure linting (ruff)
- [ ] Set up pytest with basic config
- [ ] Add CLAUDE.md / README with setup instructions

## Learn first
See [LEARNING.md](docs/LEARNING.md) → sections 1 (Python), 2 (Git)" \
  --json number --jq '.number')
echo "Epic 1 created: #$E1"

gh issue create --repo $REPO \
  --title "Initialize Git repo with .gitignore and pyproject.toml" \
  --label "story,learning" \
  --body "## Story
As a developer, I want a clean project structure so that I can start building without setup friction.

## Acceptance criteria
- [ ] Git repo initialized
- [ ] .gitignore covers .venv/, .env, __pycache__, *.db, dist/, node_modules/
- [ ] pyproject.toml defines project name, Python version, and empty dependencies list
- [ ] README.md has basic setup instructions

## Learn first
- [Git - The Simple Guide](https://rogerdudler.github.io/git-guide/)
- [Python Packaging Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

Part of Epic #$E1"

gh issue create --repo $REPO \
  --title "Set up Python virtual environment and install core dependencies" \
  --label "story,learning" \
  --body "## Story
As a developer, I want all dependencies pinned and installable with one command.

## Acceptance criteria
- [ ] .venv created with Python 3.12+
- [ ] pyproject.toml lists: fastapi, uvicorn, sqlmodel, pydantic-settings, passlib[bcrypt], python-jose[cryptography], httpx, pyyaml, psycopg[binary]
- [ ] \`pip install -e .\` installs everything

## Learn first
- [Python Packaging Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

Part of Epic #$E1"

gh issue create --repo $REPO \
  --title "Configure ruff linter and pytest" \
  --label "story" \
  --body "## Story
As a developer, I want consistent code style enforced automatically.

## Acceptance criteria
- [ ] ruff configured in pyproject.toml (line-length 100, target py312)
- [ ] pytest configured with testpaths=[\"tests\"]
- [ ] \`pytest tests/\` runs without errors (even with no tests yet)

Part of Epic #$E1"

echo ""
echo "=== EPIC 2: Database Layer ==="
E2=$(gh issue create --repo $REPO \
  --title "Epic 2: Database Layer" \
  --label "epic" \
  --body "Define the data models and database connection. Use SQLite locally, PostgreSQL in production.

## Outcome
The app can create tables and persist data on first startup.

## Stories
- [ ] Configure database session (SQLite dev / Postgres prod)
- [ ] Define User model
- [ ] Define Profile model
- [ ] Define Assessment model
- [ ] Wire init_db() into app startup

## Learn first
See [LEARNING.md](docs/LEARNING.md) → section 5 (Databases)" \
  --json number --jq '.number')
echo "Epic 2 created: #$E2"

gh issue create --repo $REPO \
  --title "Configure database session with SQLite/Postgres support" \
  --label "story,learning" \
  --body "## Story
As a developer, I want the database URL to be swappable via environment variable so I can use SQLite locally and Postgres in production.

## Acceptance criteria
- [ ] DATABASE_URL read from settings (default: sqlite:///./local.db)
- [ ] SQLModel engine created from URL
- [ ] get_session() dependency yields a session and closes it after
- [ ] init_db() creates all tables on startup

## Learn first
- [SQLModel Tutorial](https://sqlmodel.tiangolo.com/tutorial/)
- [SQLModel with FastAPI](https://sqlmodel.tiangolo.com/tutorial/fastapi/)

Part of Epic #$E2"

gh issue create --repo $REPO \
  --title "Define User, Profile, and Assessment models" \
  --label "story,learning" \
  --body "## Story
As a developer, I want typed database models so data is validated before it's stored.

## Acceptance criteria
- [ ] User: id, email (unique), password_hash, created_at
- [ ] Profile: id, user_id (FK), display_name, title, level, scorecard_role, company, tech_context
- [ ] Assessment: id, user_id (FK), self_report, result_json, overall_band, created_at
- [ ] Relationships defined (User → Profile one-to-one, User → Assessments one-to-many)

## Learn first
- [SQLModel — Table Models](https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/)
- [SQLModel — Relationships](https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/)

Part of Epic #$E2"

echo ""
echo "=== EPIC 3: Authentication ==="
E3=$(gh issue create --repo $REPO \
  --title "Epic 3: Authentication (JWT)" \
  --label "epic" \
  --body "Implement secure registration, login, and token-based auth so only the right user sees their data.

## Outcome
A user can register, receive a JWT, and use it to access protected endpoints.

## Stories
- [ ] Password hashing with bcrypt
- [ ] JWT create/decode utilities
- [ ] POST /api/auth/register
- [ ] POST /api/auth/login
- [ ] require_user dependency

## Learn first
See [LEARNING.md](docs/LEARNING.md) → section 6 (Authentication)" \
  --json number --jq '.number')
echo "Epic 3 created: #$E3"

gh issue create --repo $REPO \
  --title "Implement password hashing (bcrypt)" \
  --label "story,learning" \
  --body "## Story
As a developer, I want passwords stored as secure hashes, never plaintext.

## Acceptance criteria
- [ ] hash_password(plain) → hashed string using passlib bcrypt
- [ ] verify_password(plain, hashed) → bool
- [ ] Unit test: hash != plain, verify returns True for correct password, False for wrong

## Learn first
- [Passlib Docs](https://passlib.readthedocs.io/en/stable/narr/quickstart.html)
- [Real Python — Hashing Passwords](https://realpython.com/python-hash-table/)

Part of Epic #$E3"

gh issue create --repo $REPO \
  --title "Implement JWT token creation and decoding" \
  --label "story,learning" \
  --body "## Story
As a developer, I want to issue signed tokens on login and validate them on every protected request.

## Acceptance criteria
- [ ] create_access_token(user_id) → signed JWT string (7-day expiry, HS256)
- [ ] decode_token(token) → user_id (int) or raises ValueError
- [ ] Secret key read from settings.SECRET_KEY
- [ ] Unit test: decode(create(id)) == id, expired token raises, tampered token raises

## Learn first
- [jwt.io Introduction](https://jwt.io/introduction)
- [FastAPI OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

Part of Epic #$E3"

gh issue create --repo $REPO \
  --title "Implement POST /api/auth/register and POST /api/auth/login" \
  --label "story,learning" \
  --body "## Story
As a user, I want to create an account and log in to receive a token I can use for the rest of the session.

## Acceptance criteria
- [ ] POST /api/auth/register: {email, password} → 201 {access_token, token_type}
- [ ] Returns 409 if email already registered
- [ ] POST /api/auth/login: {email, password} → 200 {access_token, token_type}
- [ ] Returns 401 if email not found or password wrong
- [ ] API tests cover both happy paths and error cases

## Learn first
- [FastAPI — Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [FastAPI — Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)

Part of Epic #$E3"

gh issue create --repo $REPO \
  --title "Implement require_user dependency (Bearer token auth)" \
  --label "story,learning" \
  --body "## Story
As a developer, I want a reusable FastAPI dependency that extracts the user from the Bearer token so every protected route gets the current user automatically.

## Acceptance criteria
- [ ] HTTPBearer reads Authorization header
- [ ] decode_token extracts user_id
- [ ] Session lookup returns User object
- [ ] Returns 401 with WWW-Authenticate: Bearer if token missing/invalid
- [ ] All protected routes use Depends(require_user)

## Learn first
- [FastAPI — Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI — Security](https://fastapi.tiangolo.com/tutorial/security/)

Part of Epic #$E3"

echo ""
echo "=== EPIC 4: Profile & History API ==="
E4=$(gh issue create --repo $REPO \
  --title "Epic 4: Profile & History API" \
  --label "epic" \
  --body "CRUD endpoints for user profile and read endpoint for assessment history.

## Outcome
A logged-in user can manage their profile and retrieve past assessments.

## Stories
- [ ] GET /api/profile
- [ ] PUT /api/profile (create or update)
- [ ] GET /api/history

## Learn first
See [LEARNING.md](docs/LEARNING.md) → section 7 (REST API Design)" \
  --json number --jq '.number')
echo "Epic 4 created: #$E4"

gh issue create --repo $REPO \
  --title "Implement GET /api/profile and PUT /api/profile" \
  --label "story,learning" \
  --body "## Story
As a user, I want to save my role and level so the AI knows how to score me.

## Acceptance criteria
- [ ] GET /api/profile → 200 with ProfileOut schema (or 404 if not created yet)
- [ ] PUT /api/profile → upsert (create if not exists, update if exists) → 200 ProfileOut
- [ ] ProfileOut: display_name, title, level, scorecard_role, company, tech_context
- [ ] Requires Bearer auth
- [ ] API tests: create, update, verify isolation between users

## Learn first
- [FastAPI — SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [HTTP Methods — PUT vs POST](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/PUT)

Part of Epic #$E4"

gh issue create --repo $REPO \
  --title "Implement GET /api/history" \
  --label "story" \
  --body "## Story
As a user, I want to see my past assessments to track my progress over time.

## Acceptance criteria
- [ ] GET /api/history → list of assessments ordered by created_at desc
- [ ] Each item: id, created_at, self_report, overall_band, result_json
- [ ] Only returns the current user's assessments (no data leakage)
- [ ] Returns empty list if no assessments yet
- [ ] Requires Bearer auth

Part of Epic #$E4"

echo ""
echo "=== EPIC 5: AI Assessment Engine ==="
E5=$(gh issue create --repo $REPO \
  --title "Epic 5: AI Assessment Engine" \
  --label "epic" \
  --body "The core intelligence: scorecard design, prompt engineering, LLM integration, and structured output parsing.

## Outcome
Given a self-report text + role, the engine returns a scored AssessResult with dimensions, bands, and recommendations.

## Stories
- [ ] Design scorecard YAML structure
- [ ] Implement scorecard for all roles/levels
- [ ] LLM client abstraction (Gemini + Stub)
- [ ] Prompt builder
- [ ] Response parser and validator
- [ ] assess() service function

## Learn first
See [LEARNING.md](docs/LEARNING.md) → section 8 (LLM Integration)" \
  --json number --jq '.number')
echo "Epic 5 created: #$E5"

gh issue create --repo $REPO \
  --title "Design scorecard YAML structure and implement for all 17 roles" \
  --label "story,learning" \
  --body "## Story
As a developer, I want role/level-specific scoring criteria defined in a config file so they can be updated without changing code.

## Acceptance criteria
- [ ] YAML structure: role_key → dimensions → Below/Meets/Exceeds descriptors + aggregation
- [ ] 17 roles covered: trainee/junior/mid/senior/staff/principal for QA and Dev, plus 5 PO levels
- [ ] 6 dimensions per role
- [ ] Scorecard loaded once via @lru_cache
- [ ] Unit test: all 17 keys load without error

## Learn first
- [PyYAML Docs](https://pyyaml.org/wiki/PyYAMLDocumentation)

Part of Epic #$E5"

gh issue create --repo $REPO \
  --title "Implement LLM client abstraction (Gemini + Stub)" \
  --label "story,learning" \
  --body "## Story
As a developer, I want to swap LLM providers without changing business logic, and use a stub in tests.

## Acceptance criteria
- [ ] LLMClient base class with complete_json(system, user, temperature) → str
- [ ] GeminiClient: calls Gemini REST API via httpx
- [ ] StubClient: returns hardcoded valid JSON (for tests, no API key needed)
- [ ] get_llm_client() factory reads LLM_PROVIDER from settings
- [ ] Unit test: StubClient returns parseable JSON

## Learn first
- [HTTPX Docs](https://www.python-httpx.org/)
- [Gemini API Quickstart](https://ai.google.dev/gemini-api/docs/quickstart)

Part of Epic #$E5"

gh issue create --repo $REPO \
  --title "Implement prompt builder and response parser" \
  --label "story,learning" \
  --body "## Story
As a developer, I want a prompt that reliably produces structured JSON output matching the AssessResult schema.

## Acceptance criteria
- [ ] build_prompt(req, role) → (system_prompt, user_prompt)
- [ ] System prompt: role-agnostic, instructs to grade against SCORECARD section
- [ ] User prompt: includes scorecard, title, level, company/tech context, self-report
- [ ] parse_result(raw_json) → AssessResult (validated by Pydantic)
- [ ] Handles ```json fences in LLM output
- [ ] Unit test with StubClient returns valid AssessResult

## Learn first
- [Gemini — Prompting Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- [Gemini — Structured Output](https://ai.google.dev/gemini-api/docs/structured-output)
- [Pydantic — Model Validation](https://docs.pydantic.dev/latest/concepts/models/)

Part of Epic #$E5"

echo ""
echo "=== EPIC 6: Assess Endpoint ==="
E6=$(gh issue create --repo $REPO \
  --title "Epic 6: POST /api/assess Endpoint" \
  --label "epic" \
  --body "Wire the AI engine into a protected REST endpoint that reads user profile, runs assessment, and persists history.

## Outcome
An authenticated user POSTs their self-report text and gets back a scored AssessResult. The assessment is saved to history.

## Stories
- [ ] Define AssessInput and AssessResult schemas
- [ ] Implement POST /api/assess
- [ ] API test (with StubClient)

Part of Epic — no separate epic ticket needed." \
  --json number --jq '.number')
echo "Epic 6 created: #$E6"

gh issue create --repo $REPO \
  --title "Implement POST /api/assess with auth, profile lookup, and history persistence" \
  --label "story,learning" \
  --body "## Story
As a user, I want to submit my self-assessment text and receive AI-scored feedback immediately, with the result saved automatically.

## Acceptance criteria
- [ ] POST /api/assess: {self_report} → AssessResult JSON
- [ ] Requires Bearer auth
- [ ] Returns 400 if user has no profile yet
- [ ] Reads scorecard_role, title, level, company, tech_context from stored profile
- [ ] Calls assess() service with correct role
- [ ] Persists Assessment record to DB after scoring
- [ ] Returns 502 with LLM error detail if Gemini fails
- [ ] API test with StubClient: full round-trip without live LLM

## Learn first
- [FastAPI — Dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)
- [FastAPI — Error handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)

Part of Epic #$E6"

echo ""
echo "=== EPIC 7: Frontend (React) ==="
E7=$(gh issue create --repo $REPO \
  --title "Epic 7: React Frontend" \
  --label "epic" \
  --body "Build a React + TypeScript + Vite + Tailwind frontend that calls the JSON API.

## Outcome
A user can register, log in, set their profile, submit a self-assessment, and view history — all in the browser.

## Stories
- [ ] Vite + React + TypeScript + Tailwind setup
- [ ] API client (fetch + JWT)
- [ ] ProtectedRoute component
- [ ] Login page
- [ ] Register page
- [ ] Profile page (role/level dropdowns)
- [ ] Assess page (tips + textarea + result display)
- [ ] History page

## Learn first
See [LEARNING.md](docs/LEARNING.md) → section 12 (React)" \
  --json number --jq '.number')
echo "Epic 7 created: #$E7"

gh issue create --repo $REPO \
  --title "Set up Vite + React + TypeScript + Tailwind CSS" \
  --label "story,learning" \
  --body "## Story
As a developer, I want a working React development environment with hot reload and Tailwind CSS.

## Acceptance criteria
- [ ] frontend/ directory with package.json, vite.config.ts, tsconfig.json
- [ ] Tailwind CSS configured (postcss.config.js, tailwind.config.js)
- [ ] \`npm run dev\` starts dev server at localhost:5173
- [ ] \`npm run build\` produces dist/ without errors
- [ ] Vite proxy: /api → http://localhost:8000

## Learn first
- [Vite Getting Started](https://vitejs.dev/guide/)
- [Tailwind CSS Installation](https://tailwindcss.com/docs/installation)
- [React.dev Quick Start](https://react.dev/learn)

Part of Epic #$E7"

gh issue create --repo $REPO \
  --title "Build Login and Register pages" \
  --label "story,learning" \
  --body "## Story
As a user, I want to create an account and log in from a clean form page.

## Acceptance criteria
- [ ] /login page: email + password form → calls POST /api/auth/login → stores JWT → redirects to /
- [ ] /register page: email + password form → calls POST /api/auth/register → redirects to /profile
- [ ] Error message shown on bad credentials
- [ ] Already-authenticated users redirected away from login/register
- [ ] Loading state on submit button

## Learn first
- [React — useState](https://react.dev/reference/react/useState)
- [React Router — useNavigate](https://reactrouter.com/en/main/hooks/use-navigate)
- [fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)

Part of Epic #$E7"

gh issue create --repo $REPO \
  --title "Build Profile page with role/level dropdowns" \
  --label "story" \
  --body "## Story
As a user, I want to select my role and level from dropdowns so the AI knows how to score me.

## Acceptance criteria
- [ ] GET /api/profile on mount to pre-fill form
- [ ] Role dropdown: QA Engineer / Product Owner / Developer
- [ ] Level dropdown changes based on role selection
- [ ] Title field auto-fills on role+level change but remains editable
- [ ] PUT /api/profile on save
- [ ] Success and error feedback
- [ ] Requires auth (redirect to /login if no token)

Part of Epic #$E7"

gh issue create --repo $REPO \
  --title "Build Assess page with tips and result display" \
  --label "story" \
  --body "## Story
As a user, I want to paste my self-assessment text, submit it, and see scored results with recommendations.

## Acceptance criteria
- [ ] Collapsible role-specific writing tips (loaded from profile's scorecard_role)
- [ ] Textarea for self-report text
- [ ] POST /api/assess on submit
- [ ] Shows: overall band, dimension scores with band badges, recommendations
- [ ] Loading state during assessment (can take 5–10 seconds)
- [ ] Error message if assessment fails

Part of Epic #$E7"

gh issue create --repo $REPO \
  --title "Build History page" \
  --label "story" \
  --body "## Story
As a user, I want to see all my past assessments so I can track improvement over time.

## Acceptance criteria
- [ ] GET /api/history on mount
- [ ] List of assessments: date, overall band badge, first 2 lines of self-report
- [ ] Click to expand full result (dimensions + recommendations)
- [ ] Empty state message if no history
- [ ] Requires auth

Part of Epic #$E7"

echo ""
echo "=== EPIC 8: Testing ==="
E8=$(gh issue create --repo $REPO \
  --title "Epic 8: Automated Testing" \
  --label "epic" \
  --body "Write a test suite that covers auth, API endpoints, and the assessment engine — runnable without a live LLM or database.

## Outcome
\`pytest tests/\` passes in CI with no external dependencies.

## Stories
- [ ] Unit tests: security (hash/verify, JWT)
- [ ] Unit tests: assessor with StubClient
- [ ] API tests: auth endpoints
- [ ] API tests: profile and history endpoints
- [ ] API tests: assess endpoint (StubClient)
- [ ] Test database isolation (in-memory SQLite)

## Learn first
See [LEARNING.md](docs/LEARNING.md) → section 9 (Testing)" \
  --json number --jq '.number')
echo "Epic 8 created: #$E8"

gh issue create --repo $REPO \
  --title "Unit tests for auth security and JWT" \
  --label "story,learning" \
  --body "## Story
As a developer, I want unit tests for the security layer so I catch regressions before they reach users.

## Acceptance criteria
- [ ] hash_password / verify_password: correct password passes, wrong fails
- [ ] create_access_token / decode_token: round-trip works, tampered token raises, expired raises
- [ ] No database or HTTP calls in these tests

## Learn first
- [pytest Getting Started](https://docs.pytest.org/en/stable/getting-started.html)
- [ArjanCodes — pytest](https://www.youtube.com/watch?v=cHYq1MRoyI0)

Part of Epic #$E8"

gh issue create --repo $REPO \
  --title "API tests for all endpoints using TestClient and in-memory DB" \
  --label "story,learning" \
  --body "## Story
As a developer, I want integration tests that hit real HTTP endpoints with a real (in-memory) database so I can catch contract bugs.

## Acceptance criteria
- [ ] Fixtures: test app with SQLite in-memory DB, TestClient, StubClient for LLM
- [ ] Auth: register + login happy path, duplicate email 409, wrong password 401
- [ ] Profile: GET 404 before creation, PUT creates, GET returns after creation
- [ ] Assess: 400 without profile, returns AssessResult with StubClient, persists to history
- [ ] History: empty list initially, one item after assess
- [ ] User isolation: user A cannot see user B's history

## Learn first
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html)

Part of Epic #$E8"

echo ""
echo "=== EPIC 9: Deployment ==="
E9=$(gh issue create --repo $REPO \
  --title "Epic 9: Deployment (Render + Neon)" \
  --label "epic" \
  --body "Package and deploy the backend (Docker → Render) and frontend (Vite build → Render Static Site) with Neon PostgreSQL.

## Outcome
The app is live at a public URL, zero cost, auto-deploys from the main branch.

## Stories
- [ ] Write Dockerfile for FastAPI backend
- [ ] Set up Neon PostgreSQL database
- [ ] Deploy backend to Render Web Service
- [ ] Deploy frontend to Render Static Site
- [ ] Configure environment variables
- [ ] Verify end-to-end on production URL

## Learn first
See [LEARNING.md](docs/LEARNING.md) → sections 10 (Docker) and 11 (Deployment)" \
  --json number --jq '.number')
echo "Epic 9 created: #$E9"

gh issue create --repo $REPO \
  --title "Write Dockerfile for FastAPI backend" \
  --label "story,learning" \
  --body "## Story
As a developer, I want a Dockerfile that packages the app so it runs identically on Render as it does locally.

## Acceptance criteria
- [ ] Base image: python:3.12-slim
- [ ] Copies pyproject.toml and app/ separately to leverage layer caching
- [ ] RUN pip install . installs all dependencies
- [ ] CMD runs uvicorn on 0.0.0.0:\$PORT
- [ ] \`docker build . && docker run -p 8000:8000\` works locally

## Learn first
- [Docker — Get Started](https://docs.docker.com/get-started/)
- [TechWorld — Docker Tutorial](https://www.youtube.com/watch?v=3c-iBn73dDE)
- [Dockerfile Best Practices](https://docs.docker.com/build/building/best-practices/)

Part of Epic #$E9"

gh issue create --repo $REPO \
  --title "Set up Neon PostgreSQL and connect from FastAPI" \
  --label "story,learning" \
  --body "## Story
As a developer, I want a free persistent database in the cloud that the Render backend connects to.

## Acceptance criteria
- [ ] Neon project created, database URL copied
- [ ] DATABASE_URL uses postgresql+psycopg:// prefix (for psycopg3)
- [ ] Backend starts and creates tables on first deploy
- [ ] .env has DATABASE_URL (not committed to git)

## Learn first
- [Neon Quickstart](https://neon.tech/docs/get-started-with-neon/signing-up)
- [Neon — Connect from Python](https://neon.tech/docs/guides/python)

Part of Epic #$E9"

gh issue create --repo $REPO \
  --title "Deploy backend to Render and frontend to Render Static Site" \
  --label "story,learning" \
  --body "## Story
As a user, I want to access the app at a public URL without running anything locally.

## Acceptance criteria
- [ ] render.yaml defines both services (web + static)
- [ ] Backend: auto-deploys from main, DATABASE_URL and GEMINI_API_KEY set in dashboard
- [ ] Frontend: buildCommand = cd frontend && npm install && npm run build, staticPublishPath = frontend/dist
- [ ] SPA routing works (/* rewrites to /index.html)
- [ ] End-to-end test: register → profile → assess → history all work on live URL

## Learn first
- [Render Docs — Web Services](https://docs.render.com/web-services)
- [Render Docs — Static Sites](https://docs.render.com/static-sites)

Part of Epic #$E9"

echo ""
echo "All issues created! Now:"
echo "1. Go to https://github.com/sergsol/PerformanceAssistant/issues to see them"
echo "2. Create a GitHub Project board at https://github.com/sergsol/PerformanceAssistant/projects"
echo "3. Add all issues to the board and organize by Epic"
