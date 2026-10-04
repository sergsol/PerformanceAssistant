import { refreshAccessToken } from './auth'

const BASE = import.meta.env.VITE_API_URL ?? ''

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

// FastAPI returns `detail` as a string for HTTPException but as an array of
// {loc, msg, ...} objects for 422 validation errors. Turn either into text.
function formatDetail(detail: unknown, fallback: string): string {
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    const msgs = detail
      .map((d) => (d && typeof d === 'object' && 'msg' in d ? String((d as { msg: unknown }).msg) : ''))
      .filter(Boolean)
    if (msgs.length) return msgs.join('; ')
  }
  return fallback
}

const NETWORK_ERROR_MESSAGE =
  "Can't reach the server. It may be waking up (free hosting) — please try again in a minute."

async function apiFetchRaw<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('access_token')
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  }
  if (token) headers['Authorization'] = `Bearer ${token}`
  let res: Response
  try {
    res = await fetch(`${BASE}${path}`, { ...options, headers })
  } catch {
    throw new ApiError(0, NETWORK_ERROR_MESSAGE)
  }
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new ApiError(res.status, formatDetail(body.detail, res.statusText || 'Request failed'))
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
