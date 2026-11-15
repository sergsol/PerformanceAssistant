import { useState, FormEvent } from 'react'
import { Navigate } from 'react-router-dom'
import Nav from '../components/Nav'
import { assess } from '../api/assess'
import { ApiError } from '../api/client'
import { useSelection } from '../context/SelectionContext'
import { findRole } from '../data/roles'
import { tipsFor } from '../data/tips'
import type { AssessResult } from '../types'

const BAND_COLOR: Record<string, string> = {
  Below: 'bg-red-100 text-red-800',
  Meets: 'bg-emerald-100 text-emerald-800',
  Exceeds: 'bg-indigo-100 text-indigo-800',
}

export default function Assess() {
  const [text, setText] = useState('')
  const [result, setResult] = useState<AssessResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showTips, setShowTips] = useState(false)
  const { selection } = useSelection()

  // Nothing chosen yet (e.g. deep link): start at the role selector.
  const role = selection ? findRole(selection.scorecardKey) : null
  if (!selection || !role) return <Navigate to="/" replace />

  const tips = tipsFor(selection.scorecardKey)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setLoading(true); setError(''); setResult(null)
    try {
      const r = await assess({
        self_report: text,
        scorecard_role: selection!.scorecardKey,
        company: selection!.company || null,
        tech_context: selection!.techContext || null,
      })
      setResult(r)
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Something went wrong')
    } finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <Nav />
      <main className="max-w-3xl mx-auto px-4 py-6">
        <h1 className="text-xl font-medium mb-1">Your self-assessment</h1>
        <p className="text-sm text-slate-600 mb-4">
          Assessed against <span className="font-medium">{role.level.title}</span> expectations.
        </p>
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
            name="self_report"
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
                <div key={d.dimension} className="bg-white border border-slate-200 rounded-lg px-4 py-3">
                  <div className="flex items-start sm:items-center gap-3">
                    <span className="flex-1 text-sm font-medium">{d.dimension}</span>
                    <span className={`text-xs font-medium px-2.5 py-1 rounded shrink-0 ${BAND_COLOR[d.band]}`}>{d.band}</span>
                  </div>
                  {d.evidence.length > 0 && (
                    <div className="mt-2">
                      <p className="text-xs font-medium text-emerald-700 mb-1">What supported this score</p>
                      <ul className="text-sm text-slate-700 space-y-1">
                        {d.evidence.map((ev, i) => (
                          <li key={i} className="flex gap-2"><span className="text-emerald-600 shrink-0">✓</span>{ev}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {d.evidence.length === 0 && d.band === 'Below' && (
                    <p className="mt-2 text-sm text-slate-500 italic">No evidence found for this dimension in what you wrote.</p>
                  )}
                  {d.gap && (
                    <div className="mt-2 bg-amber-50 border border-amber-100 rounded-lg px-3 py-2">
                      <p className="text-xs font-medium text-amber-800 mb-0.5">To reach the next band</p>
                      <p className="text-sm text-amber-900">{d.gap}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {result.recommendations.length > 0 && (
              <div className="bg-slate-900 text-white rounded-xl p-4">
                <p className="text-sm font-medium mb-2">Your action plan for next cycle</p>
                <ul className="text-sm space-y-2">
                  {result.recommendations.map((r, i) => (
                    <li key={i} className="flex gap-2.5">
                      <span className="shrink-0 w-5 h-5 rounded-full bg-white/15 flex items-center justify-center text-xs">{i + 1}</span>
                      {r}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
