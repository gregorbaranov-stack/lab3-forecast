import { ChartPanel } from '../../components/ChartPanel'
import { TEMPERATURE_SPECS } from './config'
import type { AnalysisResponse } from '../../types'

export function TemperatureChart({ result }: { result: AnalysisResponse }) {
  return (
    <ChartPanel
      id="temperature-chart"
      title="Температура и прогноз"
      yTitle="°C"
      labels={result.labels}
      series={result.series}
      forecastLabels={result.forecast.labels}
      forecastSeries={result.forecast.series}
      specs={TEMPERATURE_SPECS}
    />
  )
}
