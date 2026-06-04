import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    // Слушать на всех интерфейсах (включая WireGuard), а не только localhost.
    // Vite напечатает Network-URL — по нему и открывать приложение удалённо.
    host: true,
    port: 5173,
    proxy: {
      // Запросы /api проксируются на локальный бэкенд. Благодаря этому наружу
      // (через WireGuard) достаточно открыть только порт 5173 — бэкенд
      // остаётся на localhost, CORS не требуется.
      '/api': 'http://localhost:8000',
    },
  },
  preview: {
    host: true,
    port: 4173,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
