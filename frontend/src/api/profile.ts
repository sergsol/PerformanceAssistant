import { fetchWithRetry } from './client'
import type { Profile } from '../types'
export const getProfile = () => fetchWithRetry<Profile>('/api/profile')
export const updateProfile = (data: Profile) =>
  fetchWithRetry<Profile>('/api/profile', { method: 'PUT', body: JSON.stringify(data) })
