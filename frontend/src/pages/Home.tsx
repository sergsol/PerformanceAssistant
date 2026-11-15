import { useState, FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import Nav from '../components/Nav'
import { useSelection } from '../context/SelectionContext'
import { ROLE_GROUPS, findRole } from '../data/roles'

export default function Home() {
  const navigate = useNavigate()
  const { selection, setSelection } = useSelection()
  const initial = selection ? findRole(selection.scorecardKey) : null
  const [roleId, setRoleId] = useState(initial?.group.id ?? '')
  const [levelKey, setLevelKey] = useState(initial?.level.key ?? '')
  const [company, setCompany] = useState(selection?.company ?? '')
  const [techContext, setTechContext] = useState(selection?.techContext ?? '')

  const group = ROLE_GROUPS.find(g => g.id === roleId)

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!levelKey) return
    setSelection({ scorecardKey: levelKey, company: company.trim(), techContext: techContext.trim() })
    navigate('/assess')
  }

  const inputCls = 'w-full border border-slate-300 rounded-lg px-3 py-2.5 text-base bg-white'
  const labelCls = 'block text-sm font-medium text-slate-700 mb-1'

  return (
    <div className="min-h-screen bg-slate-50">
      <Nav />
      <main className="max-w-3xl mx-auto px-4 py-6">
        <h1 className="text-2xl font-medium mb-1">How is your performance really going?</h1>
        <p className="text-sm text-slate-600 mb-6">
          Pick your role and level, describe what you did this cycle, and get an honest read on whether
          it reads as Below, Meets, or Exceeds expectations. No account needed.
        </p>

        <form onSubmit={handleSubmit} className="space-y-5">
          <fieldset>
            <legend className={labelCls}>1. Your role</legend>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {ROLE_GROUPS.map(g => (
                <label key={g.id}
                  className={`cursor-pointer rounded-lg border px-3 py-3 text-sm bg-white has-[:checked]:border-slate-900 has-[:checked]:ring-1 has-[:checked]:ring-slate-900 hover:border-slate-400 ${roleId === g.id ? 'border-slate-900 ring-1 ring-slate-900' : 'border-slate-200'}`}>
                  <input type="radio" name="role" value={g.id} checked={roleId === g.id} className="sr-only"
                    onChange={() => { setRoleId(g.id); setLevelKey('') }} />
                  <span className="block font-medium">{g.label}</span>
                  <span className="block text-xs text-slate-500 mt-0.5">{g.blurb}</span>
                </label>
              ))}
            </div>
          </fieldset>

          <div>
            <label htmlFor="level" className={labelCls}>2. Your level</label>
            <select id="level" name="level" value={levelKey} onChange={e => setLevelKey(e.target.value)}
              disabled={!group} required className={inputCls}>
              <option value="" disabled>{group ? '— Select level —' : '— Select a role first —'}</option>
              {group?.levels.map(l => <option key={l.key} value={l.key}>{l.title}</option>)}
            </select>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label htmlFor="company" className={labelCls}>Company <span className="text-slate-400 font-normal">(optional)</span></label>
              <input id="company" name="company" value={company} maxLength={200} onChange={e => setCompany(e.target.value)}
                placeholder="Acme Corp" className={inputCls} />
            </div>
            <div>
              <label htmlFor="tech_context" className={labelCls}>Domain / tech context <span className="text-slate-400 font-normal">(optional)</span></label>
              <input id="tech_context" name="tech_context" value={techContext} maxLength={300} onChange={e => setTechContext(e.target.value)}
                placeholder="e.g. fintech payments, mobile SDK" className={inputCls} />
            </div>
          </div>

          <button disabled={!levelKey}
            className="w-full sm:w-auto bg-slate-900 text-white rounded-lg px-6 py-3 text-base font-medium disabled:opacity-60">
            Continue
          </button>
        </form>

        <p className="text-xs text-slate-500 mt-8">
          A coaching and rehearsal tool, not an HR system: it has no view of manager feedback or company calibration.
        </p>
      </main>
    </div>
  )
}
