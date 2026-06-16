import { Plotly } from '../plotly'

interface Props {
  graphId: string
  filename: string
}

export function ExportButton({ graphId, filename }: Props) {
  function download(format: 'png' | 'svg') {
    const gd = document.getElementById(graphId)
    if (!gd) return
    Plotly.downloadImage(gd, { format, filename, width: 1200, height: 600 })
  }
  return (
    <div className="export">
      <span className="export__label">Экспорт графика:</span>
      <button className="btn btn--ghost btn--sm" onClick={() => download('png')}>
        PNG
      </button>
      <button className="btn btn--ghost btn--sm" onClick={() => download('svg')}>
        SVG
      </button>
    </div>
  )
}
