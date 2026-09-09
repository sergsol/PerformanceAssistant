import { useState, useEffect } from 'react'
import { Outlet, useLocation, Navigate } from 'react-router-dom'
import { getProfile } from '../api/profile'
import { useProfileCtx } from '../context/ProfileContext'

export default function ProtectedRoute() {
  const { pathname } = useLocation()
  const { profileComplete, markProfileComplete } = useProfileCtx()
  const [checked, setChecked] = useState(profileComplete)

  useEffect(() => {
    if (profileComplete) { setChecked(true); return }
    getProfile()
      .then(p => { if (p.display_name) markProfileComplete(); setChecked(true) })
      .catch(() => setChecked(true))
  }, [profileComplete, markProfileComplete])

  if (!checked) return null
  // Redirect to profile if incomplete and not already there
  if (!profileComplete && pathname !== '/profile') return <Navigate to="/profile" replace />

  return <Outlet />
}
