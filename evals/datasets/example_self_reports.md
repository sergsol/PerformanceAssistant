# Example Self-Assessment Prompts

## Senior QA — Strong (covers all 6 dimensions)

Use this to test a well-rounded Senior submission that should score Meets/Exceeds
across multiple dimensions.

---

This cycle I led quality for the Creative Engine ad rendering pipeline. I designed
and implemented a contract-testing layer between the ad server and renderer using
schemathesis against our OpenAPI spec, which caught a breaking schema change before
it reached staging — that change would have silently dropped click events on ~12%
of impressions.

I wrote the test strategy doc for the Q3 SDK release: identified the top 5 risk
areas (bid response parsing, viewability signals, MRAID compliance, memory on
low-end Android, and timeout behaviour under poor network), mapped them to test
layers, and got sign-off from the PM and mobile lead before any code was written.
Two of those risk areas had no existing coverage; I added targeted API and
device-farm tests for both.

I mentored one junior QA on property-based testing with Hypothesis — we spent
three sessions together, they now own the fuzzing suite for the bid parser
independently, and it found two edge-case crashes in the first week.

I presented our quality metrics (defect escape rate, test coverage delta, flaky
test trend) in the sprint review for the first time. The team agreed to add a
flakiness threshold as a PR gate based on that data.

I also refactored our shared Playwright fixture library to eliminate a 40-second
per-test setup overhead by reusing authenticated sessions, cutting the full UI
suite runtime from 18 minutes to 6.

---

## Senior QA — Execution only (should score Meets-trending-Below)

Use this to verify the anti-inflation rule: tests + bugs alone must never Exceed.

---

I write tests and report bugs. This cycle I added 30 automated API tests and filed
12 bug reports. All tests are passing and the coverage numbers went up.

---

## Senior QA — Below expected (should score mostly Below)

Use this to verify the model correctly identifies underperformance at Senior level.

---

This cycle I mostly picked up whatever tickets were assigned to me. I ran manual
regression tests before each release and flagged a few UI issues I noticed. I
attended the sprint meetings and synced with developers when I had questions about
requirements. I didn't write any automated tests this cycle because I wasn't sure
which framework the team wanted to use, so I waited for guidance. A couple of the
bugs I reported were marked as "by design" by the product team, which was
surprising. I also started reading about test automation online to get up to speed.
