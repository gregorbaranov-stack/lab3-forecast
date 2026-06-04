import { Plot } from '../plotly'
import { ExportButton } from './ExportButton'

export interface SeriesSpec {
  key: string
  label: string
  color: string
}

interface Props {
  id: string
  title: string
  yTitle: string
  labels: string[]
  series: Record<string, number[]>
  forecastLabels: string[]
  forecastSeries: Record<string, number[]>
  specs: SeriesSpec[]
}

export function ChartPanel({
  id,
  title,
  yTitle,
  labels,
  series,
  forecastLabels,
  forecastSeries,
  specs,
}: Props) {
  const data: any[] = []
  for (const spec of specs) {
    const factY = series[spec.key] ?? []
    // Фактический ряд — сплошная линия.
    data.push({
      x: labels,
      y: factY,
      type: 'scatter',
      mode: 'lines+markers',
      name: spec.label,
      line: { color: spec.color, width: 2 },
      marker: { size: 5 },
    })
    // Прогноз — пунктир того же цвета, соединён с последней фактической точкой.
    const fc = forecastSeries[spec.key] ?? []
    if (fc.length) {
      data.push({
        x: [labels[labels.length - 1], ...forecastLabels],
        y: [factY[factY.length - 1], ...fc],
        type: 'scatter',
        mode: 'lines+markers',
        name: `${spec.label} (прогноз)`,
        line: { color: spec.color, width: 2, dash: 'dot' },
        marker: { size: 6, symbol: 'circle-open' },
      })
    }
  }

  // Заголовок вынесен в HTML над графиком (см. ниже), поэтому в самой раскладке
  // Plotly его нет — это исключает наложение заголовка на легенду при переносе
  // легенды на узких (мобильных) экранах.
  const layout: any = {
    margin: { t: 64, r: 16, b: 40, l: 56 },
    xaxis: {
      type: 'date',
      rangeslider: { visible: true }, // перетаскиванием выбирается период
    },
    yaxis: { title: { text: yTitle } },
    legend: { orientation: 'h', yanchor: 'bottom', y: 1.02, x: 0, xanchor: 'left' },
    hovermode: 'x unified',
  }

  const config: any = {
    responsive: true,
    displaylogo: false,
    toImageButtonOptions: { format: 'png', filename: id },
  }

  return (
    <div className="card chart-panel">
      <div className="chart-panel__bar">
        <h3 className="chart-panel__title">{title}</h3>
        <ExportButton graphId={id} filename={id} />
      </div>
      <Plot
        divId={id}
        data={data}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '460px' }}
        useResizeHandler
      />
    </div>
  )
}
