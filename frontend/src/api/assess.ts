import { fetchWithRetry } from './client'
import type { AssessResult } from '../types'
export const assess = (self_report: string) =>
  fetchWithRetry<AssessResult>('/api/assess', { method: 'POST', body: JSON.stringify({ self_report }) })
