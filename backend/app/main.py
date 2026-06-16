"""Точка входа FastAPI-приложения."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import router

app = FastAPI(title="Анализ и прогнозирование статистических данных", version="1.0")

# Разрешаем запросы с dev-сервера Vite.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root() -> dict:
    return {"status": "ok", "service": "lab3-forecast-api"}
