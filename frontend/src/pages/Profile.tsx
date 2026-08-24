import { useState, useEffect, FormEvent } from 'react'
import Nav from '../components/Nav'
import { getProfile, updateProfile } from '../api/profile'
import { ApiError } from '../api/client'
import type { Profile as ProfileType } from '../types'
import { useProfileCtx } from '../context/ProfileContext'

interface RoleLevel { key: string; label: string; title: string }
interface RoleGroup { label: string; levels: RoleLevel[] }

const ROLES: Record<string, RoleGroup> = {
  qa: {
    label: 'QA Engineer',
    levels: [
      { key: 'trainee_qa', label: 'Trainee', title: 'Trainee QA Engineer' },
      { key: 'junior_qa', label: 'Junior', title: 'Junior QA Engineer' },
      { key: 'mid_qa', label: 'Mid', title: 'QA Engineer' },
      { key: 'senior_qa', label: 'Senior', title: 'Senior QA Engineer' },
      { key: 'staff_qa', label: 'Staff', title: 'Staff QA Engineer' },
      { key: 'principal_qa', label: 'Principal', title: 'Principal QA Engineer' },
    ],
  },
  po: {
    label: 'Product Owner',
    levels: [
      { key: 'associate_po', label: 'Associate', title: 'Associate Product Owner' },
      { key: 'po', label: 'PO', title: 'Product Owner' },
      { key: 'senior_po', label: 'Senior', title: 'Senior Product Owner' },
      { key: 'lead_po', label: 'Lead', title: 'Lead Product Owner' },
      { key: 'principal_po', label: 'Principal', title: 'Principal Product Owner' },
    ],
  },
  dev: {
    label: 'Developer',
    levels: [
      { key: 'trainee_dev', label: 'Trainee', title: 'Trainee Developer' },
      { key: 'junior_dev', label: 'Junior', title: 'Junior Developer' },
      { key: 'mid_dev', label: 'Mid', title: 'Developer' },
      { key: 'senior_dev', label: 'Senior', title: 'Senior Developer' },
      { key: 'staff_dev', label: 'Staff', title: 'Staff Developer' },
      { key: 'principal_dev', label: 'Principal', title: 'Principal Developer' },
    ],
  },
}

function roleFromKey(key: string): { role: string; level: RoleLevel } | null {
  for (const [roleId, group] of Object.entries(ROLES)) {
    const level = group.levels.find(l => l.key === key)
    if (level) return { role: roleId, level }
  }
  return null
}

export default function Profile() {
  const [form, setForm] = useState<ProfileType>({
    display_name: '', title: '', level: '',
    scorecard_role: '', company: null, tech_context: null,
  })
  const [selectedRole, setSelectedRole] = useState('')
  const [selectedLevelKey, setSelectedLevelKey] = useState('')
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { profileComplete, markProfileComplete } = useProfileCtx()

  useEffect(() => {
    getProfile()
      .then(p => {
        setForm(p)
        const found = roleFromKey(p.scorecard_role)
        if (found) { setSelectedRole(found.role); setSelectedLevelKey(found.level.key) }
      })
      .catch(() => {}) // 404 = no profile yet, that's fine
  }, [])

  function handleRoleChange(role: string) {
    setSelectedRole(role)
    setSelectedLevelKey('')
    setForm(f => ({ ...f, scorecard_role: '', title: '', level: '' }))
  }

  function handleLevelChange(levelKey: string) {
    setSelectedLevelKey(levelKey)
    const level = ROLES[selectedRole].levels.find(l => l.key === levelKey)!
    setForm(f => ({ ...f, scorecard_role: levelKey, title: level.title, level: level.label }))
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setLoading(true); setError(''); setSaved(false)
    try {
      await updateProfile(form)
      setSaved(true)
      markProfileComplete()
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Something went wrong')
    } finally { setLoading(false) }
  }

  const inputCls = 'w-full border border-slate-300 rounded-lg px-3 py-2.5 text-base bg-white'
  const labelCls = 'block text-sm font-medium text-slate-700 mb-1'

  return (
    <div className="min-h-screen bg-slate-50">
      <Nav />
      <main className="max-w-3xl mx-auto px-4 py-6">
        <h1 className="text-xl font-medium mb-6">Profile</h1>
        {!profileComplete && (
          <p className="text-sm text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2 mb-4">
            Fill in the required fields and save your profile before starting an assessment.
          </p>
        )}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className={labelCls}>Display name</label>
            <input value={form.display_name} onChange={e => setForm(f => ({ ...f, display_name: e.target.value }))}
              placeholder="Your name" required className={inputCls} />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className={labelCls}>Role</label>
              <select value={selectedRole} onChange={e => handleRoleChange(e.target.value)} required className={inputCls}>
                <option value="" disabled>— Select role —</option>
                {Object.entries(ROLES).map(([k, v]) => <option key={k} value={k}>{v.label}</option>)}
              </select>
            </div>
            <div>
              <label className={labelCls}>Level</label>
              <select value={selectedLevelKey} onChange={e => handleLevelChange(e.target.value)} required disabled={!selectedRole} className={inputCls}>
                <option value="" disabled>— Select level —</option>
                {selectedRole && ROLES[selectedRole].levels.map(l => <option key={l.key} value={l.key}>{l.label}</option>)}
              </select>
            </div>
          </div>
          <div>
            <label className={labelCls}>Job title</label>
            <input value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))}
              className={inputCls} />
          </div>
          <div>
            <label className={labelCls}>Company <span className="text-slate-400 font-normal">(optional)</span></label>
            <input value={form.company ?? ''} onChange={e => setForm(f => ({ ...f, company: e.target.value || null }))}
              placeholder="Acme Corp" className={inputCls} />
          </div>
          <div>
            <label className={labelCls}>Tech context <span className="text-slate-400 font-normal">(optional)</span></label>
            <input value={form.tech_context ?? ''} onChange={e => setForm(f => ({ ...f, tech_context: e.target.value || null }))}
              placeholder="e.g. ad-tech / mobile SDK / fintech payments" className={inputCls} />
            <p className="text-xs text-slate-500 mt-1">Domain or product context — helps the AI calibrate industry norms</p>
          </div>
          {error && <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">{error}</p>}
          {saved && <p className="text-sm text-emerald-700 bg-emerald-50 border border-emerald-200 rounded-lg px-3 py-2">Profile saved</p>}
          <button disabled={loading}
            className="bg-slate-900 text-white rounded-lg px-4 py-3 text-base font-medium disabled:opacity-60 w-full sm:w-auto">
            {loading ? 'Saving…' : 'Save profile'}
          </button>
        </form>
      </main>
    </div>
  )
}
