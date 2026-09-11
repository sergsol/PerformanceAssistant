const BASE = import.meta.env.VITE_API_URL ?? ''
const SESSION_STORAGE_KEY = 'anonymous_session_id'
const LEGACY_USER_STORAGE_KEY = 'anonymous_user_id'

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message)
  }
}

function getAnonymousIdentity(): { sessionId: string; legacyUserId: string | null } {
  const legacyUserId = localStorage.getItem(LEGACY_USER_STORAGE_KEY)
  let sessionId = localStorage.getItem(SESSION_STORAGE_KEY) ?? legacyUserId
  if (!sessionId) {
    sessionId = `session_${crypto.randomUUID()}`
  }
  localStorage.setItem(SESSION_STORAGE_KEY, sessionId)
  if (legacyUserId && legacyUserId !== sessionId) {
    localStorage.setItem(LEGACY_USER_STORAGE_KEY, sessionId)
  }
  return { sessionId, legacyUserId }
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const { sessionId, legacyUserId } = getAnonymousIdentity()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'X-Session-Id': sessionId,
    ...(options.headers as Record<string, string>),
  }
  if (legacyUserId) headers['X-User-Id'] = legacyUserId
  const res = await fetch(`${BASE}${path}`, { ...options, headers })
  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }))
    throw new ApiError(res.status, body.detail ?? res.statusText)
  }
  return res.json()
}
