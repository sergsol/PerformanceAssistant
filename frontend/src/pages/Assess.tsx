import { useState, useEffect, FormEvent } from 'react'
import Nav from '../components/Nav'
import { assess } from '../api/assess'
import { getProfile } from '../api/profile'
import { ApiError } from '../api/client'
import type { AssessResult, Profile } from '../types'

const BAND_COLOR: Record<string, string> = {
  Below: 'bg-red-100 text-red-800',
  Meets: 'bg-emerald-100 text-emerald-800',
  Exceeds: 'bg-indigo-100 text-indigo-800',
}

interface Tip { weak: string; strong: string }

const TIPS: Record<string, Tip[]> = {
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

export default function Assess() {
  const [text, setText] = useState('')
  const [result, setResult] = useState<AssessResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [profile, setProfile] = useState<Profile | null>(null)
  const [showTips, setShowTips] = useState(false)

  useEffect(() => { getProfile().then(setProfile).catch(() => {}) }, [])

  const tips = profile ? TIPS[TIPS_KEY[profile.scorecard_role] ?? 'qa_senior'] : []

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setLoading(true); setError(''); setResult(null)
    try {
      const r = await assess(text)
      setResult(r)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Something went wrong')
    } finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Nav />
      <main className="max-w-3xl mx-auto px-4 py-6">
        {tips.length > 0 && (
          <div className="mb-4">
            <button onClick={() => setShowTips(!showTips)}
              className="flex items-center gap-2 text-sm text-slate-600 hover:text-slate-900">
              <span>{showTips ? '▾' : '▸'}</span>
              Tips for a stronger self assessment
            </button>
            {showTips && (
              <div className="mt-3 grid grid-cols-1 sm:grid-cols-2 gap-3">
                {tips.map((tip, i) => (
                  <div key={i} className="rounded-lg border border-slate-200 overflow-hidden text-sm">
                    <div className="bg-red-50 px-3 py-2 text-red-800">
                      <span className="font-medium">Instead of:</span> {tip.weak}
                    </div>
                    <div className="bg-emerald-50 px-3 py-2 text-emerald-800">
                      <span className="font-medium">Write:</span> {tip.strong}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3">
          <textarea
            value={text}
            onChange={e => setText(e.target.value)}
            rows={8}
            required
            placeholder="Describe what you've been working on this performance cycle — include specific examples, numbers, and outcomes where you can."
            className="w-full border border-slate-300 rounded-lg px-3 py-3 text-base bg-white resize-y"
          />
          <button disabled={loading || !text.trim()}
            className="w-full sm:w-auto bg-slate-900 text-white rounded-lg px-6 py-3 text-base font-medium disabled:opacity-60">
            {loading ? 'Assessing…' : 'Get assessment'}
          </button>
        </form>

        {error && <p className="mt-4 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">{error}</p>}

        {result && (
          <div className="mt-6">
            <div className={`rounded-xl p-4 mb-4 ${result.trending ? 'bg-amber-50 border border-amber-200' : 'bg-white border border-slate-200'}`}>
              <p className="text-sm text-slate-600">Overall verdict</p>
              <p className="text-2xl font-medium">
                {result.overall_band}{result.trending && ` — trending ${result.trending}`}
              </p>
              <p className="text-sm text-slate-700 mt-2">{result.overall_summary}</p>
            </div>

            <p className="text-sm text-slate-600 mb-2">By dimension</p>
            <div className="space-y-2 mb-4">
              {result.dimensions.map(d => (
                <div key={d.dimension} className="flex items-start sm:items-center gap-3 bg-white border border-slate-200 rounded-lg px-4 py-3">
                  <span className="flex-1 text-sm">{d.dimension}</span>
                  <span className={`text-xs font-medium px-2.5 py-1 rounded shrink-0 ${BAND_COLOR[d.band]}`}>{d.band}</span>
                </div>
              ))}
            </div>

            {result.recommendations.length > 0 && (
              <div className="bg-slate-100 rounded-xl p-4">
                <p className="text-sm text-slate-600 mb-2">Recommendations</p>
                <ul className="list-disc list-inside text-sm space-y-1">
                  {result.recommendations.map((r, i) => <li key={i}>{r}</li>)}
                </ul>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
