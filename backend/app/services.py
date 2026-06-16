"""Сервис анализа и реестр вариантов.

- DIP: AnalysisService зависит от абстракции ForecastStrategy, а не от
  конкретной реализации.
- OCP: новый вариант задания добавляется одной строкой в реестр VARIANTS,
  существующий код при этом не меняется.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from .datasets import CurrencyDataset, Dataset, TemperatureDataset
from .forecasting import ForecastStrategy
from .statistics import (
    CurrencyStatistics,
    StatisticsCalculator,
    TemperatureStatistics,
)

# Реестр вариантов: ключ -> (класс датасета, класс статистики).
# Добавление варианта = новая строка здесь (принцип OCP).
VARIANTS: dict[str, tuple[type[Dataset], type[StatisticsCalculator]]] = {
    "currency": (CurrencyDataset, CurrencyStatistics),
    "temperature": (TemperatureDataset, TemperatureStatistics),
}

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DEMO_FILES = {
    "currency": DATA_DIR / "currency_month.json",
    "temperature": DATA_DIR / "temperature_month.json",
}


class DatasetFactory:
    """Фабрика: создаёт датасет и калькулятор по ключу варианта (реестр)."""

    @staticmethod
    def available() -> list[dict]:
        return [{"key": key, "title": ds.title} for key, (ds, _) in VARIANTS.items()]

    @staticmethod
    def create(variant: str, raw: list[dict]) -> tuple[Dataset, StatisticsCalculator]:
        if variant not in VARIANTS:
            raise ValueError(f"Неизвестный вариант: {variant}")
        dataset_cls, stats_cls = VARIANTS[variant]
        return dataset_cls.from_raw(raw), stats_cls()


def load_demo(variant: str) -> list[dict]:
    """Загружает демонстрационный набор данных варианта."""
    path = DEMO_FILES.get(variant)
    if not path or not path.exists():
        raise ValueError(f"Нет демо-данных для варианта {variant}")
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def _next_labels(last_label: str, horizon: int) -> list[str]:
    """Подписи будущих дат, продолжая ряд по дням."""
    try:
        last = datetime.strptime(last_label, "%Y-%m-%d")
    except ValueError:
        return [f"+{i + 1}" for i in range(horizon)]
    return [(last + timedelta(days=i + 1)).strftime("%Y-%m-%d") for i in range(horizon)]


class AnalysisService:
    """Оркестрация анализа: данные -> таблица, ряды, статистика, прогноз."""

    def __init__(self, forecaster: ForecastStrategy) -> None:
        self._forecaster = forecaster

    def analyze(
        self,
        variant: str,
        raw: Optional[list[dict]],
        window: int,
        horizon: int,
        period: Optional[dict] = None,
    ) -> dict:
        if raw is None:
            raw = load_demo(variant)
        raw = self._apply_period(raw, period)
        dataset, stats = DatasetFactory.create(variant, raw)

        labels = dataset.labels()
        series = dataset.series()
        forecast_series = {
            name: self._forecaster.forecast(values, window, horizon)
            for name, values in series.items()
        }
        forecast_labels = _next_labels(labels[-1], horizon) if labels else []

        return {
            "dataset": variant,
            "labels": labels,
            "table": dataset.to_table(),
            "series": series,
            "statistics": stats.compute(dataset),
            "forecast": {
                "window": window,
                "horizon": horizon,
                "labels": forecast_labels,
                "series": forecast_series,
            },
        }

    @staticmethod
    def _apply_period(raw: list[dict], period: Optional[dict]) -> list[dict]:
        if not period:
            return raw
        start = period.get("start")
        end = period.get("end")

        def in_range(item: dict) -> bool:
            day = item.get("date", "")
            if start and day < start:
                return False
            if end and day > end:
                return False
            return True

        filtered = [item for item in raw if in_range(item)]
        return filtered or raw
