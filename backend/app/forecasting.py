"""Стратегии прогнозирования (паттерн «Стратегия»).

ForecastStrategy — абстракция; добавление нового метода прогноза не требует
изменения существующего кода (принцип OCP).
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class ForecastStrategy(ABC):
    """Контракт стратегии прогнозирования числового ряда."""

    @abstractmethod
    def forecast(self, series: list[float], window: int, horizon: int) -> list[float]:
        """Возвращает horizon прогнозных значений по ряду series."""


class MovingAverageForecaster(ForecastStrategy):
    """Экстраполяция по скользящей средней.

    Прогноз каждого следующего значения — это среднее последних ``window``
    значений ряда; полученный прогноз добавляется в ряд и участвует в расчёте
    последующих значений (рекурсивная скользящая средняя, как в методичке).
    """

    def forecast(self, series: list[float], window: int, horizon: int) -> list[float]:
        if window < 1:
            raise ValueError("Размер окна n должен быть не меньше 1")
        if window > len(series):
            raise ValueError("Размер окна n не может превышать число точек ряда")
        if horizon < 0:
            raise ValueError("Горизонт N должен быть неотрицательным")

        extended = list(series)
        predictions: list[float] = []
        for _ in range(horizon):
            window_values = extended[-window:]
            next_value = sum(window_values) / len(window_values)
            predictions.append(next_value)
            extended.append(next_value)
        return predictions
