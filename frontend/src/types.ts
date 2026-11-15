export interface AssessInput {
  self_report: string
  scorecard_role: string
  company?: string | null
  tech_context?: string | null
}

export interface DimensionScore {
  dimension: string
  band: 'Below' | 'Meets' | 'Exceeds'
  evidence: string[]
  gap: string | null
}

export interface AssessResult {
  overall_band: 'Below' | 'Meets' | 'Exceeds'
  overall_summary: string
  trending: string | null
  dimensions: DimensionScore[]
  recommendations: string[]
}
