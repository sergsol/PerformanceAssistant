import { useEffect, useState } from 'react'
import Nav from '../components/Nav'
import { getHistory } from '../api/history'
import type { HistoryItem, AssessResult } from '../types'

const BAND_COLOR: Record<string, string> = {
  Below: 'bg-red-100 text-red-800',
  Meets: 'bg-emerald-100 text-emerald-800',
  Exceeds: 'bg-indigo-100 text-indigo-800',
}

export default function History() {
  const [items, setItems] = useState<HistoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [open, setOpen] = useState<number | null>(null)

  useEffect(() => {
    getHistory().then(setItems).finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-slate-50">
      <Nav />
      <main className="max-w-3xl mx-auto px-4 py-6">
        <h1 className="text-xl font-medium mb-4">History</h1>
        {loading && <p className="text-slate-500 text-sm">Loading…</p>}
        {!loading && items.length === 0 && (
          <p className="text-slate-500 text-sm">No assessments yet. Go to <a href="/" className="underline">Assess</a> to get started.</p>
        )}
        <div className="space-y-3">
          {items.map(item => {
            const result: AssessResult = JSON.parse(item.result_json)
            const isOpen = open === item.id
            return (
              <div key={item.id} className="bg-white border border-slate-200 rounded-xl p-4">
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <span className={`text-xs font-medium px-2.5 py-1 rounded ${BAND_COLOR[item.overall_band] ?? ''}`}>
                      {item.overall_band}
                    </span>
                    <span className="text-sm text-slate-500 ml-3">
                      {new Date(item.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <button onClick={() => setOpen(isOpen ? null : item.id)}
                    className="text-sm text-slate-500 hover:text-slate-900">
                    {isOpen ? 'Hide' : 'View'}
                  </button>
                </div>
                {!isOpen && <p className="text-sm text-slate-600 mt-2 line-clamp-2">{item.self_report}</p>}
                {isOpen && (
                  <div className="mt-4 border-t border-slate-100 pt-4 space-y-3">
                    <div>
                      <p className="text-xs font-medium text-slate-500 mb-1">What you wrote</p>
                      <p className="text-sm text-slate-700 whitespace-pre-wrap bg-slate-50 rounded-lg px-3 py-2">{item.self_report}</p>
                    </div>
                    <p className="text-sm text-slate-700">{result.overall_summary}</p>
                    <div className="space-y-2">
                      {result.dimensions.map(d => (
                        <div key={d.dimension} className="flex items-center gap-3 bg-slate-50 rounded-lg px-3 py-2">
                          <span className="flex-1 text-sm">{d.dimension}</span>
                          <span className={`text-xs font-medium px-2.5 py-1 rounded shrink-0 ${BAND_COLOR[d.band]}`}>{d.band}</span>
                        </div>
                      ))}
                    </div>
                    {result.recommendations.length > 0 && (
                      <div className="bg-slate-100 rounded-xl p-3">
                        <p className="text-sm text-slate-600 mb-2">Recommendations</p>
                        <ul className="list-disc list-inside text-sm space-y-1">
                          {result.recommendations.map((r, i) => <li key={i}>{r}</li>)}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </main>
    </div>
  )
}
