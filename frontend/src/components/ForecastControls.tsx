import type { Period } from '../types'

interface Props {
  n: number
  horizon: number
  period: Period
  onChangeN: (v: number) => void
  onChangeHorizon: (v: number) => void
  onChangePeriod: (p: Period) => void
  onSubmit: () => void
  disabled?: boolean
}

export function ForecastControls({
  n,
  horizon,
  period,
  onChangeN,
  onChangeHorizon,
  onChangePeriod,
  onSubmit,
  disabled,
}: Props) {
  return (
    <div className="card controls">
      <div className="control">
        <label>Окно скользящей средней (n)</label>
        <input type="number" min={1} value={n} onChange={(e) => onChangeN(Number(e.target.value))} />
      </div>
      <div className="control">
        <label>Горизонт прогноза (N)</label>
        <input
          type="number"
          min={0}
          value={horizon}
          onChange={(e) => onChangeHorizon(Number(e.target.value))}
        />
      </div>
      <div className="control">
        <label>Период с</label>
        <input
          type="date"
          value={period.start ?? ''}
          onChange={(e) => onChangePeriod({ ...period, start: e.target.value || undefined })}
        />
      </div>
      <div className="control">
        <label>по</label>
        <input
          type="date"
          value={period.end ?? ''}
          onChange={(e) => onChangePeriod({ ...period, end: e.target.value || undefined })}
        />
      </div>
      <button className="btn btn--primary" onClick={onSubmit} disabled={disabled}>
        Построить
      </button>
    </div>
  )
}
