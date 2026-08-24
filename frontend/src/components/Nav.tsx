import { Link, useLocation, useNavigate } from 'react-router-dom'
import { logout } from '../api/auth'

const NAV = [{ to: '/', label: 'Assess' }, { to: '/history', label: 'History' }, { to: '/profile', label: 'Profile' }]

export default function Nav() {
  const { pathname } = useLocation()
  const navigate = useNavigate()
  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="max-w-3xl mx-auto px-4 py-3 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm">
        <Link to="/" className="font-medium">Performance Assistant</Link>
        {NAV.map(({ to, label }) => (
          <Link key={to} to={to}
            className={pathname === to ? 'text-slate-900 font-medium' : 'text-slate-500 hover:text-slate-900'}>
            {label}
          </Link>
        ))}
        <button onClick={() => { logout(); navigate('/login') }}
          className="ml-auto text-slate-500 hover:text-slate-900">Log out</button>
      </div>
    </nav>
  )
}
