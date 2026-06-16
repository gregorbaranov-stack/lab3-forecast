import { useState } from 'react'
import './styles.css'
import { TemperatureModule } from './modules/TemperatureModule'
import { CurrencyModule } from './modules/CurrencyModule'


type TabKey = string

interface TabDef {
  key: TabKey
  title: string
  render: () => JSX.Element
}

// Общий связанный интерфейс команды.
const TABS: TabDef[] = [
  { key: 'temperature', title: 'Температура', render: () => <TemperatureModule /> },
  { key: 'currency', title: 'Курсы валют', render: () => <CurrencyModule /> },
]

export default function App() {
  const [active, setActive] = useState<TabKey>(TABS[0]?.key ?? '')
  const current = TABS.find((t) => t.key === active) ?? TABS[0]

  return (
    <div className="app">
      <header className="app__header">
        <h1>Анализ и прогнозирование статистических данных</h1>
        <p className="app__subtitle">Командный проект • ЛР №3 «Системы контроля версий»</p>
      </header>
      <nav className="app__nav">
        {TABS.map((t) => (
          <button
            key={t.key}
            className={'tab' + (t.key === active ? ' tab--active' : '')}
            onClick={() => setActive(t.key)}
          >
            {t.title}
          </button>
        ))}
      </nav>
      <main className="app__main">
        {current ? current.render() : <p className="placeholder">Выберите раздел</p>}
      </main>
    </div>
  )
}
