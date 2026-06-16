interface Change {
  value: number
  date: string | null
}

interface CurrencyStat {
  max_gain: Change
  max_loss: Change
}

interface Props {
  statistics: Record<string, CurrencyStat>
}

export function ChangeSummary({ statistics }: Props) {
  const entries = Object.entries(statistics)
  return (
    <div className="card summary">
      <h3>Максимальные дневные изменения рубля</h3>
      <table className="summary-table">
        <thead>
          <tr>
            <th>Валюта</th>
            <th>Макс. укрепление, ₽</th>
            <th>День</th>
            <th>Макс. ослабление, ₽</th>
            <th>День</th>
          </tr>
        </thead>
        <tbody>
          {entries.map(([currency, st]) => (
            <tr key={currency}>
              <td>{currency}</td>
              <td>{st.max_gain.value}</td>
              <td>{st.max_gain.date ?? '—'}</td>
              <td>{st.max_loss.value}</td>
              <td>{st.max_loss.date ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
