# Product Requirements Document — Performance Assistant

## Problem

Engineers at mid-to-large companies write performance self-assessments once or twice a year but consistently struggle with three things:
1. **They undersell themselves** — they write activities ("wrote tests") instead of outcomes ("cut defect escape rate 40%")
2. **They don't know the bar** — they don't know what "Meets" vs "Exceeds" looks like at their specific role and level
3. **They get vague feedback** — managers give generic comments rather than specific evidence-based gaps

The result: engineers with strong actual performance get rated lower than they deserve because they can't articulate their impact.

---

## Solution

An AI-powered web app where engineers paste their self-assessment text and receive:
- A score across 6 dimensions calibrated to their role and level
- Concrete evidence quotes from their own text
- Specific recommendations to move up a band
- Writing tips before they start, tailored to their role

---

## Target Users

| Who | Context |
|---|---|
| QA Engineers (Trainee → Principal) | Want to demonstrate quality ownership, not just test execution |
| Product Owners (Associate → Principal) | Want to show strategic impact, not just ticket management |
| Software Developers (Trainee → Principal) | Want to show technical depth and cross-team influence |

Primary user: mid-level individual contributor (2–5 years experience) preparing for a review cycle.

---

## Core Features

### Must Have (MVP)
- User registration and login
- Profile: role, level, company, tech context
- AI assessment against role/level scorecard
- Scores across 6 dimensions with band (Below / Meets / Exceeds)
- Overall verdict with summary
- Concrete recommendations per dimension
- Assessment history

### Should Have
- Role/level-specific writing tips before submitting
- Mobile-friendly UI

### Nice to Have (future)
- Compare assessments across cycles (trending)
- Manager view (read-only shared link)
- Export to PDF
- Slack integration

### Out of Scope
- Automated HR system integration
- Team/org-level analytics
- Compensation recommendations

---

## Success Metrics

- User completes an assessment after first login (activation)
- User returns for a second assessment (retention)
- Assessment recommendations are acted on (qualitative, user interviews)

---

## Constraints

- Free hosting only (Render free tier + Neon free Postgres)
- No PII stored beyond email + role context
- API key never committed to source control
