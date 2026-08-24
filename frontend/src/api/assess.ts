import { apiFetch } from './client'
import type { AssessResult } from '../types'
export const assess = (self_report: string) =>
  apiFetch<AssessResult>('/api/assess', { method: 'POST', body: JSON.stringify({ self_report }) })
