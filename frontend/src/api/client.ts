const BASE = import.meta.env.VITE_API_URL ?? ''
const SESSION_STORAGE_KEY = 'anonymous_session_id'
const LEGACY_USER_STORAGE_KEY = 'anonymous_user_id'

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

function getAnonymousSessionId(): string {
  let sessionId = localStorage.getItem(SESSION_STORAGE_KEY) ?? localStorage.getItem(LEGACY_USER_STORAGE_KEY)
  if (!sessionId) {
    sessionId = `session_${crypto.randomUUID()}`
  }
  localStorage.setItem(SESSION_STORAGE_KEY, sessionId)
  localStorage.removeItem(LEGACY_USER_STORAGE_KEY)
  return sessionId
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'X-Session-Id': getAnonymousSessionId(),
    ...(options.headers as Record<string, string>),
  }
  const res = await fetch(`${BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new ApiError(res.status, body.detail ?? res.statusText)
  }
  return res.json()
}
