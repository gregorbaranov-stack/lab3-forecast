// Единый экземпляр Plotly: используется и компонентом графика, и экспортом,
// чтобы downloadImage работал над тем же DOM-узлом, что рисует график.
// Берём облегчённую сборку (basic): в ней есть линейные графики, ползунок
// диапазона и экспорт изображения — этого достаточно, а вес заметно меньше
// полного дистрибутива (важно для загрузки на мобильном через WireGuard).
import Plotly from 'plotly.js-basic-dist-min'
import createPlotlyComponent from 'react-plotly.js/factory'

export const Plot = createPlotlyComponent(Plotly)
export { Plotly }
