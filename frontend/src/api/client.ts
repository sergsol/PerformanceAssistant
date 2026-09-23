import { refreshAccessToken } from './auth'

const BASE = import.meta.env.VITE_API_URL ?? ''

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

async function apiFetchRaw<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('access_token')
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  }
  if (token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new ApiError(res.status, body.detail ?? res.statusText)
  }
  if (res.status === 204) return undefined as unknown as T
  return res.json()
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  return apiFetchRaw<T>(path, options)
}

// Use this for requests that need auto-refresh
export async function fetchWithRetry<T>(path: string, options: RequestInit = {}): Promise<T> {
  try {
    return await apiFetchRaw<T>(path, options)
  } catch (err) {
    if (err instanceof ApiError && err.status === 401) {
      const refreshed = await refreshAccessToken()
      if (refreshed) {
        return await apiFetchRaw<T>(path, options)
      }
    }
    throw err
  }
}
