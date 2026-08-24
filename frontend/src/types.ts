export interface Profile {
  display_name: string
  title: string
  level: string
  scorecard_role: string
  company: string | null
  tech_context: string | null
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

export interface HistoryItem {
  id: number
  created_at: string
  self_report: string
  overall_band: string
  result_json: string
}
