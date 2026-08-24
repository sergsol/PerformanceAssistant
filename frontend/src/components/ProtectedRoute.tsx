import { useState, useEffect } from 'react'
import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { isAuthenticated } from '../api/auth'
import { getProfile } from '../api/profile'
import { useProfileCtx } from '../context/ProfileContext'

export default function ProtectedRoute() {
  const { pathname } = useLocation()
  const { profileComplete, markProfileComplete } = useProfileCtx()
  const [checked, setChecked] = useState(profileComplete)

  useEffect(() => {
    if (profileComplete) { setChecked(true); return }
    if (!isAuthenticated()) { setChecked(true); return }
    getProfile()
      .then(p => { if (p.display_name) markProfileComplete(); setChecked(true) })
      .catch(() => setChecked(true))
  }, [])

  if (!isAuthenticated()) return <Navigate to="/login" replace />
  if (!checked) return null
  if (!profileComplete && pathname !== '/profile') return <Navigate to="/profile" replace />

  return <Outlet />
}
