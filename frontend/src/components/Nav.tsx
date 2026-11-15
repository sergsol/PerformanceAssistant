import { Link, useLocation } from 'react-router-dom'
import { useSelection } from '../context/SelectionContext'
import { findRole } from '../data/roles'

export default function Nav() {
  const { pathname } = useLocation()
  const { selection } = useSelection()
  const role = selection ? findRole(selection.scorecardKey) : null

  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="max-w-3xl mx-auto px-4 py-3 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm">
        <Link to="/" className="font-medium">Performance Assistant</Link>
        {role && pathname !== '/' && (
          <>
            <span className="text-slate-500" data-testid="current-role">{role.level.title}</span>
            <Link to="/" className="ml-auto text-slate-500 hover:text-slate-900">Change role</Link>
          </>
        )}
      </div>
    </nav>
  )
}
