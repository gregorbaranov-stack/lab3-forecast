"""Калькуляторы статистики — полиморфные метрики для каждого варианта.

StatisticsCalculator — абстракция (ISP: узкий интерфейс «посчитать метрику»);
конкретные реализации считают метрику своего варианта.
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from .datasets import Dataset


class StatisticsCalculator(ABC):
    """Контракт расчёта статистики по датасету."""

    @abstractmethod
    def compute(self, dataset: Dataset) -> dict:
        """Возвращает словарь метрик варианта."""


class CurrencyStatistics(StatisticsCalculator):
    """Максимальный дневной прирост и падение рубля относительно каждой валюты.

    Курс задан как «рублей за единицу валюты»: снижение курса означает
    укрепление рубля (прибавил), рост курса — ослабление (потерял).
    """

    def compute(self, dataset: Dataset) -> dict:
        labels = dataset.labels()
        series = dataset.series()
        result: dict = {}
        for name, values in series.items():
            best_gain = {"value": 0.0, "date": None}
            best_loss = {"value": 0.0, "date": None}
            for i in range(1, len(values)):
                delta = values[i] - values[i - 1]
                if delta < 0 and -delta > best_gain["value"]:
                    best_gain = {"value": round(-delta, 4), "date": labels[i]}
                elif delta > 0 and delta > best_loss["value"]:
                    best_loss = {"value": round(delta, 4), "date": labels[i]}
            result[name] = {"max_gain": best_gain, "max_loss": best_loss}
        return result


class TemperatureStatistics(StatisticsCalculator):
    """Дни с самым сильным и самым слабым перепадом температуры (max − min)."""

    def compute(self, dataset: Dataset) -> dict:
        labels = dataset.labels()
        series = dataset.series()
        mins = series["t_min"]
        maxs = series["t_max"]
        swings = [maxs[i] - mins[i] for i in range(len(mins))]
        if not swings:
            return {}
        strongest = max(range(len(swings)), key=lambda i: swings[i])
        weakest = min(range(len(swings)), key=lambda i: swings[i])
        return {
            "strongest_swing": {"value": round(swings[strongest], 2), "date": labels[strongest]},
            "weakest_swing": {"value": round(swings[weakest], 2), "date": labels[weakest]},
        }
