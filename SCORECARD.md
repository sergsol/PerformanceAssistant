# Senior QA Leveling Rubric (v1)

> This rubric is the **spec** for PerfReviewBot and the **ground truth** for its
> golden-dataset labels. It is authored (not copied from any single company) but
> synthesized from recurring, cross-company engineering/QA ladder patterns so it
> is both credible and fully under our control for labeling.
>
> Machine-readable version lives at `app/rubric/rubric.yaml`. This file is the
> human-readable reference we refine.

## Design principles (from the research)

- At senior level you **stop being measured by the number of tests you write and
  start being measured by the quality outcomes your team delivers.** This is the
  central axis.
- The junior→senior leap specifically expects: **proposing framework
  improvements, documenting risk-assessment methodologies, mentoring juniors,
  and presenting quality metrics to stakeholders.**
- Senior QA are **technical leaders who drive testing strategy and architecture**,
  not test executors.
- Valued engineers **tie quality to business metrics** ("affects 40% of checkout")
  rather than reporting isolated defects.
- True seniority = **preventing quality failures before they occur** (prevention
  over detection).
- Modern (2026) QA includes **AI-assisted testing** as part of the discipline —
  captured within Dimension 2.

## The core encoded judgment

Dimension 1 (execution) maxed out **alone** → overall caps at **Meets-trending-Below**
for Senior. Execution is necessary but not sufficient. The bot must not read
*volume of low-level work* as seniority.

---

## Dimension 1 — Technical execution & automation

*Writing reliable tests and using/maintaining frameworks.*

- **Below:** Writes some tests but they're flaky/shallow; relies on others to fix
  framework issues; limited automation.
- **Meets:** Writes reliable automated tests across UI/API; fluent in the team's
  framework; solid bug reports (steps, expected/actual, severity). **This is the
  ceiling for someone doing only execution work.**
- **Exceeds:** Improves the framework itself; introduces patterns others adopt;
  raises the team's automation bar.

> Note: strong Dimension 1 with empty 2–6 → overall Meets-trending-Below.

## Dimension 2 — Test strategy & quality ownership

*Owning the testing approach; shifting from detection to prevention.*

- **Below:** Follows test plans written by others; reactive; no strategy input.
- **Meets:** Owns test strategy for a feature/service; chooses appropriate test
  levels; risk-based coverage; begins preventing defects (shift-left).
- **Exceeds:** Owns quality strategy across multiple services/teams; drives
  prevention culture; introduces new practices (incl. AI-assisted testing) that
  measurably improve outcomes.

## Dimension 3 — Autonomy & scope

*How much direction is needed; how ambiguous the problems handled.*

- **Below:** Needs well-defined tasks and regular direction.
- **Meets:** Self-directed on ambiguous quality problems within their area;
  defines their own approach.
- **Exceeds:** Sets direction on org-level ambiguous problems; others take
  direction from them.

## Dimension 4 — Influence & collaboration

*Shaping how others work; communicating with stakeholders.*

- **Below:** Communicates within own tasks; little cross-team interaction.
- **Meets:** Collaborates effectively with dev/PM; presents quality metrics to
  stakeholders; influences peers on quality.
- **Exceeds:** Shifts how the team/org thinks about quality; trusted cross-team
  quality advocate; influences roadmap/process.

## Dimension 5 — Mentorship

*Growing other testers.*

- **Below:** Focused only on own work.
- **Meets:** Mentors junior testers; reviews others' tests; shares knowledge.
- **Exceeds:** Formally grows multiple engineers; raises the whole team's
  capability; creates learning resources/standards.

## Dimension 6 — Business & risk impact

*Tying quality work to business outcomes and risk.*

- **Below:** Reports issues without business context ("this button is wrong").
- **Meets:** Frames quality in business/risk terms ("this bug affects X% of
  checkout"); prioritizes by risk.
- **Exceeds:** Quantifies quality's business impact (e.g. "reduced regression
  suite time 65%"); drives risk-based decisions that change what the org ships.

---

## Overall-band aggregation (draft policy — to encode & test)

Not a simple average. Proposed rules:
- **Exceeds overall:** Exceeds in ≥3 dimensions incl. at least one of {2,4,6},
  and no dimension Below.
- **Meets overall:** Meets or better in ≥4 dimensions incl. Dimension 2.
- **Below overall:** Dimension 2 is Below, OR ≥3 dimensions Below.
- **Meets-trending-Below (the key case):** Dimension 1 Meets/Exceeds but
  Dimensions 2,4,5,6 mostly empty/Below → surfaces as "you're executing but not
  yet operating at Senior scope."

These aggregation rules are themselves unit-testable and are great parametrized
test fodder.

## Sources (industry ladder patterns synthesized)
- asserthired.com — "you stop being measured by number of tests…"; junior vs
  senior "what you do".
- Medium (Sibarani) — junior→senior leap list (framework improvements, risk
  methodology docs, mentoring, stakeholder metrics); "prevent failures before
  they occur."
- yrkan.com — seniors as technical leaders driving strategy/architecture;
  AI-assisted testing as modern QA.
- qapot.com / tryqa.com — seniors think about business impact; automation as the
  advancement lever.
