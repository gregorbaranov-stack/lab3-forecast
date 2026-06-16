interface Swing {
  value: number
  date: string | null
}

interface Props {
  statistics: { strongest_swing?: Swing; weakest_swing?: Swing }
}

export function SwingSummary({ statistics }: Props) {
  const strongest = statistics.strongest_swing
  const weakest = statistics.weakest_swing
  return (
    <div className="card summary">
      <h3>Перепад температуры (максимум − минимум)</h3>
      <ul className="summary-list">
        <li>
          Самый сильный перепад: <b>{strongest ? `${strongest.value} °C` : '—'}</b>
          {strongest?.date ? ` (${strongest.date})` : ''}
        </li>
        <li>
          Самый слабый перепад: <b>{weakest ? `${weakest.value} °C` : '—'}</b>
          {weakest?.date ? ` (${weakest.date})` : ''}
        </li>
      </ul>
    </div>
  )
}
