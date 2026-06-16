import type { AnalysisResponse, AnalyzePayload } from './types'

// По умолчанию обращаемся к API по тому же адресу, с которого открыто
// приложение (относительный путь). Vite-прокси перенаправит /api на локальный
// бэкенд — это работает и на localhost, и при доступе через WireGuard.
// При необходимости можно переопределить адрес бэкенда через VITE_API_BASE.
const BASE = (import.meta.env.VITE_API_BASE as string) ?? ''

export interface DatasetInfo {
  key: string
  title: string
}

export async function listDatasets(): Promise<DatasetInfo[]> {
  const res = await fetch(`${BASE}/api/datasets`)
  if (!res.ok) throw new Error('Не удалось получить список вариантов')
  return res.json()
}

export async function analyze(variant: string, payload: AnalyzePayload): Promise<AnalysisResponse> {
  const res = await fetch(`${BASE}/api/${variant}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    const detail = await res.json().catch(() => ({}))
    throw new Error(detail.detail ?? `Ошибка анализа (${res.status})`)
  }
  return res.json()
}

export async function loadSample(file: string): Promise<unknown[]> {
  const res = await fetch(`/sample/${file}`)
  if (!res.ok) throw new Error('Не удалось загрузить демо-данные')
  return res.json()
}
