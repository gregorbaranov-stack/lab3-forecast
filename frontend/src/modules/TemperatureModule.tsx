import { useEffect, useState } from 'react'
import { analyze, loadSample } from '../api'
import type { AnalysisResponse, Period } from '../types'
import { FileLoader } from '../components/FileLoader'
import { DataTable } from '../components/DataTable'
import { ForecastControls } from '../components/ForecastControls'
import { TemperatureChart } from './temperature/TemperatureChart'
import { SwingSummary } from './temperature/SwingSummary'

const SAMPLE = 'temperature_month.json'

export function TemperatureModule() {
  const [records, setRecords] = useState<unknown[] | null>(null)
  const [n, setN] = useState(5)
  const [horizon, setHorizon] = useState(7)
  const [period, setPeriod] = useState<Period>({})
  const [result, setResult] = useState<AnalysisResponse | null>(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function run(recs: unknown[] | null) {
    setLoading(true)
    setError('')
    try {
      const res = await analyze('temperature', { records: recs ?? undefined, n, horizon, period })
      setResult(res)
    } catch (e: any) {
      setError(e.message ?? 'Ошибка')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    run(records)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function handleSample() {
    const data = await loadSample(SAMPLE)
    setRecords(data)
    run(data)
  }

  return (
    <section className="module">
      <h2>Вариант 3 — температура в городе</h2>
      <FileLoader
        sampleFile={SAMPLE}
        onLoadFile={(r) => {
          setRecords(r)
          run(r)
        }}
        onLoadSample={handleSample}
      />
      <ForecastControls
        n={n}
        horizon={horizon}
        period={period}
        onChangeN={setN}
        onChangeHorizon={setHorizon}
        onChangePeriod={setPeriod}
        onSubmit={() => run(records)}
        disabled={loading}
      />
      {error && <div className="error">{error}</div>}
      {result && (
        <>
          <SwingSummary statistics={result.statistics} />
          <TemperatureChart result={result} />
          <DataTable table={result.table} />
        </>
      )}
    </section>
  )
}
