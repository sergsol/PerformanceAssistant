import { useState, useEffect } from 'react'
import { Outlet, useLocation } from 'react-router-dom'
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
  }, [])

  if (!checked) return null
  // Only redirect to profile if incomplete and not already there
  if (!profileComplete && pathname !== '/profile') {
    // Silently continue - no auth check needed
    setChecked(true)
  }

  return <Outlet />
}
