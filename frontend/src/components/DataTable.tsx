import type { TableData } from '../types'

interface Props {
  table: TableData
  maxRows?: number
}

export function DataTable({ table, maxRows }: Props) {
  const rows = maxRows ? table.rows.slice(0, maxRows) : table.rows
  return (
    <div className="card">
      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              {table.headers.map((h) => (
                <th key={h}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i}>
                {row.map((cell, j) => (
                  <td key={j}>{String(cell)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
