import { ROLE_GROUPS } from './roles'

export interface Tip { weak: string; strong: string }

export const TIPS: Record<string, Tip[]> = {
  qa_early: [
    { weak: 'Reported bugs', strong: 'Filed 12 bug reports; 10 accepted as-is, 3 were critical severity that blocked release' },
    { weak: 'Ran test cases', strong: 'Executed the regression suite for checkout; caught a missed edge case on declined cards not in the test plan' },
    { weak: 'Attended meetings', strong: 'Asked clarifying questions in 3 sprint plannings that caught missing acceptance criteria before dev started' },
    { weak: 'Learned the automation framework', strong: 'Wrote 5 automated tests independently; my mentor reviewed them without major revisions' },
  ],
  qa_mid: [
    { weak: 'Wrote test strategy', strong: 'Wrote the payments test strategy before dev started; 2 of 4 risk areas I flagged had zero coverage — I built tests for both' },
    { weak: 'Mentored junior QAs', strong: 'Mentored 2 junior QAs — they now independently write test strategies for small features and own their own PR reviews' },
    { weak: 'Improved the test suite', strong: 'Refactored the shared fixture library — cut the full regression suite from 18 min to 6 min, adopted by the whole team' },
    { weak: 'Collaborated with developers', strong: 'Flagged 3 quality risks in design reviews before any code was written; 2 were accepted and changed the implementation' },
  ],
  qa_senior: [
    { weak: 'Owned test strategy', strong: 'Wrote and got sign-off on the test strategy before any code was written; identified 2 risk areas with zero existing coverage' },
    { weak: 'Mentored junior QAs', strong: 'Mentored 1 junior QA on property-based testing — they now own the fuzzing suite independently; it found 2 bugs in its first week' },
    { weak: 'Improved quality metrics', strong: 'Defect escape rate dropped 40% this cycle — directly attributable to the risk-based testing approach I introduced for the team' },
    { weak: 'Shared approach with other teams', strong: 'Presented the contract-testing pattern to 3 squads; 2 adopted it and caught breaking changes before staging' },
  ],
  po_early: [
    { weak: 'Wrote requirements', strong: 'Ran 3 architect sessions to validate feasibility before writing specs; only 1 clarification needed during development' },
    { weak: 'Updated the roadmap', strong: 'Maintained the year-level roadmap and presented it to 2 enterprise customers; incorporated their feedback into Q4 prioritization' },
    { weak: 'Led product meetings', strong: 'Led 4 external customer calls and 8 internal planning sessions; resolved 3 competing stakeholder priorities with documented trade-offs' },
    { weak: 'Supported junior POs', strong: "Paired with 2 junior POs on feature breakdown — after 3 sessions, they're writing acceptance criteria independently" },
  ],
  po_senior: [
    { weak: 'Worked on product strategy', strong: 'Defined the 18-month enterprise strategy; presented it to the CPO — it shaped 3 of the 5 company OKRs for the year' },
    { weak: 'Presented to customers', strong: 'Presented the year-level roadmap to 5 enterprise customers; 2 renewed based on roadmap commitments, 1 expanded scope' },
    { weak: 'Coordinated teams', strong: 'Resolved a 6-week dependency conflict between 3 teams by proposing a phased delivery model; all teams accepted, delivery stayed on track' },
    { weak: 'Mentored junior POs', strong: 'Mentored 3 POs — 1 was promoted to Senior; the other 2 now independently own their domain roadmaps and present to stakeholders' },
  ],
  dev_early: [
    { weak: 'Wrote code for the feature', strong: 'Implemented CSV export; reviewer said it was the cleanest code from a junior this quarter — merged with no major revisions' },
    { weak: 'Wrote tests', strong: 'Wrote unit tests covering 12 edge cases including nulls, unicode, and concurrent access — caught a race condition before review' },
    { weak: 'Helped team members', strong: 'Documented the async debugging approach I learned and posted it to the team wiki — 3 teammates referenced it the same week' },
    { weak: 'Fixed bugs', strong: 'Fixed 5 bugs; for the 2 most complex, I wrote a root-cause explanation in the PR so the team could avoid the pattern in future' },
  ],
  dev_mid: [
    { weak: 'Designed the service', strong: 'Designed the token refresh flow, ran a review with 4 engineers, incorporated edge-case feedback — adopted as the team standard' },
    { weak: 'Mentored junior devs', strong: 'Mentored 2 junior devs through pairing and PR reviews — both shipped features independently this sprint that needed senior support last cycle' },
    { weak: 'Improved test coverage', strong: 'Introduced async testing patterns for our service layer; adopted by the team and found a race condition causing intermittent 500s for 6 weeks' },
    { weak: 'Worked with other teams', strong: 'Resolved an API contract conflict with 2 teams before dev started — saved an estimated 2 sprints of integration rework' },
  ],
  dev_senior: [
    { weak: 'Designed the system', strong: 'Designed the service mesh migration for payments — adopted by 2 other domains; eliminated an entire class of timeout-related incidents' },
    { weak: 'Mentored engineers', strong: 'Formally mentored 3 engineers — 2 promoted to Senior this cycle; both are now independently leading multi-team technical projects' },
    { weak: 'Improved code quality', strong: 'Introduced the error handling standard company-wide — adopted across 8 services in 6 weeks; reduced error-related support tickets by 60%' },
    { weak: 'Fixed performance issues', strong: 'Reduced API p99 latency from 4 s to 280 ms — directly tied to a 12% improvement in checkout completion rate reported by product' },
  ],
  pm: [
    { weak: 'Managed the project plan', strong: 'Delivered the platform migration on the committed date by re-sequencing 3 dependencies in week 4 and getting sponsor sign-off on the trade-off' },
    { weak: 'Reported status to stakeholders', strong: 'Introduced a one-page weekly status with RAG and top 3 risks; steering-committee surprises dropped to zero over the last 2 quarters' },
    { weak: 'Handled project risks', strong: 'Identified a vendor delivery risk 6 weeks early, negotiated a fallback, and avoided an estimated 3-week slip' },
    { weak: 'Kept the project on budget', strong: 'Held spend within 2% of the approved budget by cutting two low-value features, with sponsor approval documented' },
  ],
  prodm: [
    { weak: 'Gathered customer feedback', strong: 'Ran 15 customer interviews and a usage analysis; found that 60% of churn came from onboarding, which reshaped the quarter\'s roadmap' },
    { weak: 'Prioritized the backlog', strong: 'Replaced a request-driven backlog with 3 outcome-based themes; said no to 8 requests with documented reasoning and stakeholder buy-in' },
    { weak: 'Launched a feature', strong: 'Launched the new checkout flow with success metrics defined up front; conversion rose 7% and we iterated twice based on the data' },
    { weak: 'Worked with engineering', strong: 'Cut a 10-week scope to a 4-week first release with the tech lead, shipping on time with no mid-sprint requirement changes' },
  ],
  devops: [
    { weak: 'Maintained the pipelines', strong: 'Rebuilt the CI pipeline with caching and parallel stages: build time dropped from 25 to 8 minutes across 12 services' },
    { weak: 'Handled incidents', strong: 'Led the response to the database failover incident (recovered in 18 min), wrote the blameless postmortem, and shipped 3 follow-up fixes' },
    { weak: 'Wrote infrastructure code', strong: 'Moved all production infrastructure to Terraform modules with peer review; environment drift incidents went from monthly to none' },
    { weak: 'Helped developers deploy', strong: 'Built a self-service deploy template adopted by 5 teams; deployment frequency doubled and lead time fell from 3 days to 4 hours' },
  ],
  security: [
    { weak: 'Ran vulnerability scans', strong: 'Triaged 240 scanner findings down to 18 exploitable issues, set remediation SLAs, and brought critical mean time to fix from 40 to 9 days' },
    { weak: 'Did security reviews', strong: 'Led threat modeling for the new payments API; 4 design changes were adopted before any code was written' },
    { weak: 'Helped with an incident', strong: 'Led investigation of a credential-stuffing attack, contained it in 2 hours, and added detections that now catch the pattern automatically' },
    { weak: 'Worked on compliance', strong: 'Mapped controls to SOC 2, automated 70% of evidence collection, and passed the audit with no major findings' },
  ],
  hr: [
    { weak: 'Handled employee issues', strong: 'Resolved 12 employee relations cases within policy timelines, coached 4 managers on difficult conversations, and had no escalations to legal' },
    { weak: 'Supported hiring', strong: 'Redesigned the interview process with structured scorecards; offer acceptance rose from 62% to 81% and time-to-hire fell by 9 days' },
    { weak: 'Ran the engagement survey', strong: 'Analyzed survey results by team, partnered with 3 leaders on action plans, and lifted the engagement score 8 points in two quarters' },
    { weak: 'Managed HR processes', strong: 'Automated onboarding paperwork and equipment requests, cutting new-hire setup from 5 days to 1 with no compliance gaps' },
  ],
}

/** Tip set for a given scorecard key (e.g. "senior_qa", "mid_devops"). */
export function tipsFor(scorecardKey: string): Tip[] {
  const tierKey = TIPS_KEY[scorecardKey]
  if (tierKey) return TIPS[tierKey]
  const family = ROLE_GROUPS.find(g => g.levels.some(l => l.key === scorecardKey))
  return family ? TIPS[family.id] ?? [] : []
}

const TIPS_KEY: Record<string, string> = {
  trainee_qa: 'qa_early', junior_qa: 'qa_early',
  mid_qa: 'qa_mid',
  senior_qa: 'qa_senior', staff_qa: 'qa_senior', principal_qa: 'qa_senior',
  associate_po: 'po_early', po: 'po_early',
  senior_po: 'po_senior', lead_po: 'po_senior', principal_po: 'po_senior',
  trainee_dev: 'dev_early', junior_dev: 'dev_early',
  mid_dev: 'dev_mid',
  senior_dev: 'dev_senior', staff_dev: 'dev_senior', principal_dev: 'dev_senior',
}
