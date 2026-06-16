import { ChartPanel } from '../../components/ChartPanel'
import { CURRENCY_SPECS } from './config'
import type { AnalysisResponse } from '../../types'

export function CurrencyChart({ result }: { result: AnalysisResponse }) {
  return (
    <ChartPanel
      id="currency-chart"
      title="Курс рубля к валютам и прогноз"
      yTitle="₽ за единицу валюты"
      labels={result.labels}
      series={result.series}
      forecastLabels={result.forecast.labels}
      forecastSeries={result.forecast.series}
      specs={CURRENCY_SPECS}
    />
  )
}
