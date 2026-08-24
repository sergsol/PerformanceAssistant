# Learning Roadmap — Performance Assistant

What you need to learn to build this project from scratch.
Each section maps to a specific epic in the project. Links point to the best available resource for each topic.

---

## 1. Python Foundations
*Needed for: everything*

You already know Python, so this is just filling gaps relevant to backend development.

| Topic | Resource | Format |
|---|---|---|
| Type hints (`: str`, `list[int]`, `X \| None`) | [Real Python — Type Checking](https://realpython.com/python-type-checking/) | Article |
| Dataclasses and `__init__` patterns | [Real Python — Dataclasses](https://realpython.com/python-data-classes/) | Article |
| `async`/`await` basics | [Real Python — Async IO](https://realpython.com/async-io-python/) | Article |
| Virtual environments & `pyproject.toml` | [Python Packaging Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/) | Docs |

---

## 2. Git & GitHub
*Needed for: Epic 1 — Project Setup*

| Topic | Resource | Format |
|---|---|---|
| Git basics (commit, branch, push) | [Git - The Simple Guide](https://rogerdudler.github.io/git-guide/) | Interactive |
| GitHub flow (branches, PRs) | [GitHub Flow Guide](https://docs.github.com/en/get-started/using-github/github-flow) | Docs |
| `.gitignore` patterns | [gitignore.io](https://www.toptal.com/developers/gitignore) | Tool |
| GitHub Projects (boards, issues) | [GitHub Projects Quickstart](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/quickstart-for-projects) | Docs |

---

## 3. FastAPI
*Needed for: Epic 3 — Auth API, Epic 4 — Core API, Epic 6 — Assess Endpoint*

FastAPI is the core of this project. The official tutorial is exceptionally good — go through it in order.

| Topic | Resource | Format |
|---|---|---|
| **Full FastAPI tutorial** (start here) | [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/) | Docs + interactive |
| Path operations, request body, response model | Above tutorial — chapters 1–10 | Docs |
| Dependencies (`Depends`) | [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) | Docs |
| Security / Bearer tokens | [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/) | Docs |
| CORS middleware | [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/) | Docs |
| Testing with TestClient | [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/) | Docs |
| Video walkthrough | [ArjanCodes — FastAPI Tutorial](https://www.youtube.com/watch?v=SORiTsvnU28) | Video |

---

## 4. Pydantic (data validation)
*Needed for: Epic 3, 4, 5, 6 — all schemas*

FastAPI uses Pydantic under the hood. You define what data looks like and Pydantic validates it automatically.

| Topic | Resource | Format |
|---|---|---|
| BaseModel, field types, validators | [Pydantic Docs — Models](https://docs.pydantic.dev/latest/concepts/models/) | Docs |
| Field defaults, optional fields | [Pydantic — Fields](https://docs.pydantic.dev/latest/concepts/fields/) | Docs |
| Video intro | [Pydantic v2 Crash Course](https://www.youtube.com/watch?v=XIdQ6gO3Anc) | Video |

---

## 5. Databases — SQLModel + SQLite/PostgreSQL
*Needed for: Epic 2 — Database Layer*

SQLModel is a library that combines SQLAlchemy (database ORM) and Pydantic. You define one class that works as both a database table and an API schema.

| Topic | Resource | Format |
|---|---|---|
| **SQLModel Tutorial** (start here) | [SQLModel Official Tutorial](https://sqlmodel.tiangolo.com/tutorial/) | Docs |
| What is an ORM? | [Real Python — ORM](https://realpython.com/python-sqlite-sqlalchemy/) | Article |
| PostgreSQL basics | [PostgreSQL Tutorial](https://www.postgresqltutorial.com/) | Interactive |
| Neon (serverless Postgres) | [Neon Docs — Quickstart](https://neon.tech/docs/get-started-with-neon/signing-up) | Docs |

---

## 6. Authentication — JWT
*Needed for: Epic 3 — Auth*

JWT (JSON Web Token) is how the app proves who you are after login. You log in once, get a token, and send it with every request.

| Topic | Resource | Format |
|---|---|---|
| What is JWT? (visual explanation) | [jwt.io Introduction](https://jwt.io/introduction) | Article |
| How Bearer tokens work in HTTP | [MDN — Authorization header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Authorization) | Docs |
| Implementing JWT in FastAPI | [FastAPI — OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) | Docs |
| Password hashing with bcrypt | [Passlib Docs](https://passlib.readthedocs.io/en/stable/narr/quickstart.html) | Docs |

---

## 7. REST API Design
*Needed for: Epic 4 — Core API*

Understanding what makes a well-designed API — correct HTTP methods, status codes, and response shapes.

| Topic | Resource | Format |
|---|---|---|
| REST API concepts | [RESTful API Design — Best Practices](https://blog.pragmaticengineer.com/rest-api-design/) | Article |
| HTTP status codes | [MDN — HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) | Reference |
| OpenAPI / Swagger | [Swagger Docs](https://swagger.io/docs/specification/about/) | Docs |

---

## 8. LLM Integration
*Needed for: Epic 5 — AI Assessment Engine*

How to call a language model API and parse structured responses.

| Topic | Resource | Format |
|---|---|---|
| Google Gemini API basics | [Gemini API Quickstart](https://ai.google.dev/gemini-api/docs/quickstart) | Docs |
| Prompt engineering | [Google — Prompting Guide](https://ai.google.dev/gemini-api/docs/prompting-strategies) | Docs |
| Structured output (JSON mode) | [Gemini — JSON mode](https://ai.google.dev/gemini-api/docs/structured-output) | Docs |
| Making HTTP requests with httpx | [HTTPX Docs](https://www.python-httpx.org/) | Docs |

---

## 9. Testing — pytest + httpx
*Needed for: Epic 8 — Testing*

Testing your API endpoints programmatically so you can catch bugs before users do.

| Topic | Resource | Format |
|---|---|---|
| pytest basics | [pytest Getting Started](https://docs.pytest.org/en/stable/getting-started.html) | Docs |
| pytest video intro | [ArjanCodes — pytest](https://www.youtube.com/watch?v=cHYq1MRoyI0) | Video |
| Testing FastAPI | [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/) | Docs |
| Fixtures and test isolation | [pytest Fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) | Docs |

---

## 10. Docker
*Needed for: Epic 9 — Deployment*

Docker packages your app so it runs the same everywhere — your laptop, a server, Render.

| Topic | Resource | Format |
|---|---|---|
| What is Docker? | [Docker — Get Started](https://docs.docker.com/get-started/) | Docs + interactive |
| Writing a Dockerfile | [Dockerfile Best Practices](https://docs.docker.com/build/building/best-practices/) | Docs |
| Video intro | [TechWorld — Docker Tutorial](https://www.youtube.com/watch?v=3c-iBn73dDE) | Video |

---

## 11. Deployment — Render + Neon
*Needed for: Epic 9 — Deployment*

| Topic | Resource | Format |
|---|---|---|
| Render — deploying a Docker app | [Render Docs — Web Services](https://docs.render.com/web-services) | Docs |
| Render — static sites (React) | [Render Docs — Static Sites](https://docs.render.com/static-sites) | Docs |
| Environment variables in production | [Render — Environment Variables](https://docs.render.com/configure-environment-variables) | Docs |
| Neon — connecting from Python | [Neon Docs — Python](https://neon.tech/docs/guides/python) | Docs |

---

## 12. React (brief — for understanding, not mastery)
*Needed for: Epic 7 — Frontend*

You'll primarily use AI to write React, but understanding the basics helps you review and debug it.

| Topic | Resource | Format |
|---|---|---|
| What React is and why it exists | [React.dev — Quick Start](https://react.dev/learn) | Interactive |
| Components, props, state | [React.dev — Describing the UI](https://react.dev/learn/describing-the-ui) | Interactive |
| useEffect (data fetching) | [React.dev — Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects) | Interactive |
| React Router (navigation) | [React Router Tutorial](https://reactrouter.com/tutorials/address-book) | Interactive |
| TypeScript with React | [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/) | Reference |
| Tailwind CSS | [Tailwind CSS Docs](https://tailwindcss.com/docs/installation) | Docs |

---

## Suggested Study Order

```
Week 1:  Git & GitHub → Python type hints → FastAPI tutorial (chapters 1–15)
Week 2:  Pydantic → SQLModel tutorial → JWT concepts
Week 3:  FastAPI security → REST API design → pytest basics
Week 4:  Docker → Deployment → LLM integration
Ongoing: React (as needed when implementing the frontend)
```
