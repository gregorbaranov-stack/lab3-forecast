import { useState } from 'react'

interface Props {
  sampleFile: string
  onLoadFile: (records: unknown[]) => void
  onLoadSample: () => void
}

export function FileLoader({ sampleFile, onLoadFile, onLoadSample }: Props) {
  const [name, setName] = useState('')

  function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return
    setName(file.name)
    const reader = new FileReader()
    reader.onload = () => {
      try {
        const data = JSON.parse(String(reader.result))
        onLoadFile(Array.isArray(data) ? data : [])
      } catch {
        alert('Не удалось разобрать JSON-файл')
      }
    }
    reader.readAsText(file)
  }

  return (
    <div className="card file-loader">
      <label className="btn">
        Загрузить JSON-файл
        <input type="file" accept="application/json,.json" hidden onChange={handleFile} />
      </label>
      <button className="btn btn--ghost" onClick={onLoadSample}>
        Демо-данные ({sampleFile})
      </button>
      {name && <span className="file-loader__name">{name}</span>}
    </div>
  )
}
