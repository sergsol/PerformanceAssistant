import { apiFetch } from './client'
import type { Profile } from '../types'
export const getProfile = () => apiFetch<Profile>('/api/profile')
export const updateProfile = (data: Profile) => apiFetch<Profile>('/api/profile', { method: 'PUT', body: JSON.stringify(data) })
