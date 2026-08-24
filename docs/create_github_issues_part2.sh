#!/usr/bin/env bash
# Creates GitHub issues for Epics 6-9 (run after create_github_issues.sh)
# Usage: bash docs/create_github_issues_part2.sh

REPO="sergsol/PerformanceAssistant"

echo "=== EPIC 6: Assess Endpoint ==="
E6=$(gh issue create --repo $REPO \
  --title "Epic 6: POST /api/assess Endpoint" \
  --label "epic" \
  --body "Wire the AI engine into a protected REST endpoint that reads the user profile, runs the assessment, and persists history.

## Outcome
An authenticated user POSTs their self-report text and gets back a scored AssessResult. The result is saved automatically to history.

## Stories
- [ ] Implement POST /api/assess with auth, profile lookup, and history persistence

## Learn first
See LEARNING.md sections 3 (FastAPI) and 8 (LLM Integration)" \
  --json number --jq '.number')
echo "Epic 6: #$E6"

gh issue create --repo $REPO \
  --title "Implement POST /api/assess with auth, profile lookup, and history persistence" \
  --label "story,learning" \
  --body "## Story
As a user, I want to submit my self-assessment text and receive AI-scored feedback immediately, with the result saved automatically.

## Acceptance criteria
- [ ] POST /api/assess: {self_report} -> AssessResult JSON
- [ ] Requires Bearer auth (401 if missing/invalid)
- [ ] Returns 400 if user has no profile yet
- [ ] Reads scorecard_role, title, level, company, tech_context from stored profile
- [ ] Calls assess() service with correct role
- [ ] Persists Assessment record to DB after scoring
- [ ] Returns 502 with LLM error detail if Gemini fails
- [ ] API test with StubClient: full round-trip without live LLM

## Learn first
- https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
- https://fastapi.tiangolo.com/tutorial/handling-errors/

Part of Epic #$E6"

echo ""
echo "=== EPIC 7: React Frontend ==="
E7=$(gh issue create --repo $REPO \
  --title "Epic 7: React Frontend" \
  --label "epic" \
  --body "Build a React + TypeScript + Vite + Tailwind frontend that calls the JSON API.

## Outcome
A user can register, log in, set their profile, submit a self-assessment, and view history — all in the browser.

## Stories
- [ ] Set up Vite + React + TypeScript + Tailwind CSS
- [ ] Build Login and Register pages
- [ ] Build Profile page with role/level dropdowns
- [ ] Build Assess page with tips and result display
- [ ] Build History page

## Learn first
See LEARNING.md section 12 (React)" \
  --json number --jq '.number')
echo "Epic 7: #$E7"

gh issue create --repo $REPO \
  --title "Set up Vite + React + TypeScript + Tailwind CSS" \
  --label "story,learning" \
  --body "## Story
As a developer, I want a working React development environment with hot reload and Tailwind CSS.

## Acceptance criteria
- [ ] frontend/ directory with package.json, vite.config.ts, tsconfig.json
- [ ] Tailwind CSS configured (postcss.config.js, tailwind.config.js)
- [ ] npm run dev starts dev server at localhost:5173
- [ ] npm run build produces dist/ without errors
- [ ] Vite proxy: /api -> http://localhost:8000

## Learn first
- https://vitejs.dev/guide/
- https://tailwindcss.com/docs/installation
- https://react.dev/learn

Part of Epic #$E7"

gh issue create --repo $REPO \
  --title "Build Login and Register pages" \
  --label "story,learning" \
  --body "## Story
As a user, I want to create an account and log in from a clean form page.

## Acceptance criteria
- [ ] /login: email + password form, calls POST /api/auth/login, stores JWT, redirects to /
- [ ] /register: email + password form, calls POST /api/auth/register, redirects to /profile
- [ ] Error message shown on bad credentials
- [ ] Already-authenticated users redirected away
- [ ] Loading state on submit button

## Learn first
- https://react.dev/reference/react/useState
- https://reactrouter.com/en/main/hooks/use-navigate
- https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

Part of Epic #$E7"

gh issue create --repo $REPO \
  --title "Build Profile page with role/level dropdowns" \
  --label "story" \
  --body "## Story
As a user, I want to select my role and level so the AI knows how to score me.

## Acceptance criteria
- [ ] GET /api/profile on mount to pre-fill the form
- [ ] Role dropdown: QA Engineer / Product Owner / Developer
- [ ] Level dropdown changes based on role selection
- [ ] Title field auto-fills on role+level change but remains editable
- [ ] PUT /api/profile on save
- [ ] Success and error feedback
- [ ] Requires auth (redirect to /login if no token)

Part of Epic #$E7"

gh issue create --repo $REPO \
  --title "Build Assess page with writing tips and result display" \
  --label "story" \
  --body "## Story
As a user, I want to paste my self-assessment text, submit it, and see scored results with recommendations.

## Acceptance criteria
- [ ] Collapsible role-specific writing tips based on profile scorecard_role
- [ ] Textarea for self-report text
- [ ] POST /api/assess on submit
- [ ] Shows: overall band, dimension scores with band badges, recommendations
- [ ] Loading state during assessment (can take 5-10 seconds)
- [ ] Error message if assessment fails

Part of Epic #$E7"

gh issue create --repo $REPO \
  --title "Build History page" \
  --label "story" \
  --body "## Story
As a user, I want to see all my past assessments so I can track improvement over time.

## Acceptance criteria
- [ ] GET /api/history on mount
- [ ] List of assessments: date, overall band badge, preview of self-report
- [ ] Click to expand full result (dimensions + recommendations)
- [ ] Empty state message if no history
- [ ] Requires auth

Part of Epic #$E7"

echo ""
echo "=== EPIC 8: Testing ==="
E8=$(gh issue create --repo $REPO \
  --title "Epic 8: Automated Testing" \
  --label "epic" \
  --body "Write a test suite covering auth, API endpoints, and the assessment engine — runnable without a live LLM or real database.

## Outcome
pytest tests/ passes in CI with no external dependencies.

## Stories
- [ ] Unit tests: password hashing and JWT
- [ ] API tests: auth, profile, history, assess endpoints
- [ ] Test database isolation (in-memory SQLite)

## Learn first
See LEARNING.md section 9 (Testing)" \
  --json number --jq '.number')
echo "Epic 8: #$E8"

gh issue create --repo $REPO \
  --title "Unit tests for password hashing and JWT" \
  --label "story,learning" \
  --body "## Story
As a developer, I want unit tests for the security layer so I catch regressions before they reach users.

## Acceptance criteria
- [ ] hash_password / verify_password: correct password passes, wrong fails
- [ ] create_access_token / decode_token: round-trip works, tampered token raises, expired raises
- [ ] No database or HTTP calls in these tests

## Learn first
- https://docs.pytest.org/en/stable/getting-started.html
- https://www.youtube.com/watch?v=cHYq1MRoyI0 (ArjanCodes pytest)

Part of Epic #$E8"

gh issue create --repo $REPO \
  --title "API tests for all endpoints using TestClient and in-memory DB" \
  --label "story,learning" \
  --body "## Story
As a developer, I want integration tests that hit real HTTP endpoints with a real (in-memory) database so I can catch contract bugs.

## Acceptance criteria
- [ ] Fixtures: test app with SQLite in-memory DB, TestClient, StubClient for LLM
- [ ] Auth: register + login happy path, duplicate email 409, wrong password 401
- [ ] Profile: GET 404 before creation, PUT creates, GET returns after
- [ ] Assess: 400 without profile, returns AssessResult with StubClient, persists to history
- [ ] History: empty list initially, one item after assess
- [ ] User isolation: user A cannot see user B history

## Learn first
- https://fastapi.tiangolo.com/tutorial/testing/
- https://docs.pytest.org/en/stable/how-to/fixtures.html

Part of Epic #$E8"

echo ""
echo "=== EPIC 9: Deployment ==="
E9=$(gh issue create --repo $REPO \
  --title "Epic 9: Deployment (Render + Neon)" \
  --label "epic" \
  --body "Package and deploy the backend (Docker -> Render Web Service) and frontend (Vite build -> Render Static Site) with Neon PostgreSQL.

## Outcome
The app is live at a public URL, zero cost, auto-deploys from the main branch.

## Stories
- [ ] Write Dockerfile for FastAPI backend
- [ ] Set up Neon PostgreSQL database
- [ ] Deploy backend + frontend to Render

## Learn first
See LEARNING.md sections 10 (Docker) and 11 (Deployment)" \
  --json number --jq '.number')
echo "Epic 9: #$E9"

gh issue create --repo $REPO \
  --title "Write Dockerfile for FastAPI backend" \
  --label "story,learning" \
  --body "## Story
As a developer, I want a Dockerfile that packages the app so it runs identically on Render as locally.

## Acceptance criteria
- [ ] Base image: python:3.12-slim
- [ ] Copies pyproject.toml and app/ to leverage layer caching
- [ ] RUN pip install . installs all dependencies
- [ ] CMD runs uvicorn on 0.0.0.0:PORT
- [ ] docker build + docker run works locally

## Learn first
- https://docs.docker.com/get-started/
- https://www.youtube.com/watch?v=3c-iBn73dDE (TechWorld Docker)
- https://docs.docker.com/build/building/best-practices/

Part of Epic #$E9"

gh issue create --repo $REPO \
  --title "Set up Neon PostgreSQL and connect from FastAPI" \
  --label "story,learning" \
  --body "## Story
As a developer, I want a free persistent database in the cloud that the Render backend connects to.

## Acceptance criteria
- [ ] Neon project created, connection string copied
- [ ] DATABASE_URL uses postgresql+psycopg:// prefix (required for psycopg3)
- [ ] Backend starts and creates tables on first deploy
- [ ] .env stores DATABASE_URL locally (not committed to git)

## Learn first
- https://neon.tech/docs/get-started-with-neon/signing-up
- https://neon.tech/docs/guides/python

Part of Epic #$E9"

gh issue create --repo $REPO \
  --title "Deploy backend to Render Web Service and frontend to Render Static Site" \
  --label "story,learning" \
  --body "## Story
As a user, I want to access the app at a public URL without running anything locally.

## Acceptance criteria
- [ ] render.yaml defines both services (web + static)
- [ ] Backend: auto-deploys from main, DATABASE_URL and GEMINI_API_KEY set in dashboard
- [ ] Frontend: buildCommand = cd frontend && npm install && npm run build
- [ ] SPA routing works (/* rewrites to /index.html)
- [ ] End-to-end: register, profile, assess, history all work on live URL

## Learn first
- https://docs.render.com/web-services
- https://docs.render.com/static-sites

Part of Epic #$E9"

echo ""
echo "All done! View issues at: https://github.com/sergsol/PerformanceAssistant/issues"
echo ""
echo "Next: create a GitHub Project board at https://github.com/sergsol/PerformanceAssistant/projects"
