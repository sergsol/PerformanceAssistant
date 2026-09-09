import { Link, useLocation } from 'react-router-dom'
import { useProfileCtx } from '../context/ProfileContext'

const NAV = [{ to: '/', label: 'Assess' }, { to: '/history', label: 'History' }, { to: '/profile', label: 'Profile' }]

export default function Nav() {
  const { pathname } = useLocation()
  const { profileComplete } = useProfileCtx()

  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="max-w-3xl mx-auto px-4 py-3 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm">
        <Link to="/" className="font-medium">Performance Assistant</Link>
        {NAV.map(({ to, label }) => {
          const locked = !profileComplete && to !== '/profile'
          if (locked) {
            return (
              <span key={to} title="Complete your profile first"
                className="text-slate-300 cursor-not-allowed select-none">
                {label}
              </span>
            )
          }
          return (
            <Link key={to} to={to}
              className={pathname === to ? 'text-slate-900 font-medium' : 'text-slate-500 hover:text-slate-900'}>
              {label}
            </Link>
          )
        })}
      </div>
    </nav>
  )
}
