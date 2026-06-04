export interface TableData {
  headers: string[]
  rows: (string | number)[][]
}

export interface ForecastData {
  window: number
  horizon: number
  labels: string[]
  series: Record<string, number[]>
}

export interface AnalysisResponse {
  dataset: string
  labels: string[]
  table: TableData
  series: Record<string, number[]>
  statistics: Record<string, any>
  forecast: ForecastData
}

export interface Period {
  start?: string
  end?: string
}

export interface AnalyzePayload {
  records?: unknown[]
  n: number
  horizon: number
  period?: Period
}
