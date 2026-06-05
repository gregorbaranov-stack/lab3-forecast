import type { SeriesSpec } from '../../components/ChartPanel'

// Требование варианта 3: минимум — синий, максимум — красный.
export const TEMPERATURE_SPECS: SeriesSpec[] = [
  { key: 't_min', label: 'Мин.', color: '#1f77b4' },
  { key: 't_max', label: 'Макс.', color: '#d62728' },
  { key: 't_avg', label: 'Сред.', color: '#7f7f7f' },
]
