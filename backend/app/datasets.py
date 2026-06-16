"""Датасеты — абстракция представления данных и её реализации.

Здесь сосредоточены принципы ООП:
- абстракция: базовый класс Dataset задаёт контракт;
- наследование: CurrencyDataset и TemperatureDataset наследуют Dataset;
- полиморфизм: сервис вызывает единые методы независимо от варианта.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from pydantic import BaseModel

from .models import CurrencyRecord, TemperatureRecord


class Dataset(ABC):
    """Абстрактный датасет. Единый контракт для всех вариантов задания."""

    key: str = ""
    title: str = ""
    record_model: type[BaseModel] = BaseModel

    def __init__(self, records: Sequence[BaseModel]) -> None:
        self._records = list(records)

    @classmethod
    def from_raw(cls, raw: list[dict]) -> "Dataset":
        """Полиморфно строит датасет из «сырых» словарей через модель варианта."""
        records = [cls.record_model(**item) for item in raw]
        return cls(records)

    @property
    def records(self) -> list[BaseModel]:
        return self._records

    def labels(self) -> list[str]:
        """Подписи оси X — даты."""
        return [record.date for record in self._records]  # type: ignore[attr-defined]

    @abstractmethod
    def to_table(self) -> dict:
        """Табличное представление: {headers, rows}."""

    @abstractmethod
    def series(self) -> dict[str, list[float]]:
        """Числовые ряды для графиков и прогноза."""


class CurrencyDataset(Dataset):
    """Вариант 2 — курс рубля к доллару США и евро."""

    key = "currency"
    title = "Курсы валют"
    record_model = CurrencyRecord

    def to_table(self) -> dict:
        return {
            "headers": ["Дата", "RUB/USD", "RUB/EUR"],
            "rows": [[r.date, r.usd, r.eur] for r in self._records],  # type: ignore[attr-defined]
        }

    def series(self) -> dict[str, list[float]]:
        return {
            "USD": [r.usd for r in self._records],  # type: ignore[attr-defined]
            "EUR": [r.eur for r in self._records],  # type: ignore[attr-defined]
        }


class TemperatureDataset(Dataset):
    """Вариант 3 — температура в городе."""

    key = "temperature"
    title = "Температура"
    record_model = TemperatureRecord

    def to_table(self) -> dict:
        return {
            "headers": ["Дата", "Минимум, °C", "Максимум, °C", "Среднее, °C", "Описание"],
            "rows": [
                [r.date, r.t_min, r.t_max, r.t_avg, r.description]  # type: ignore[attr-defined]
                for r in self._records
            ],
        }

    def series(self) -> dict[str, list[float]]:
        return {
            "t_min": [r.t_min for r in self._records],  # type: ignore[attr-defined]
            "t_max": [r.t_max for r in self._records],  # type: ignore[attr-defined]
            "t_avg": [r.t_avg for r in self._records],  # type: ignore[attr-defined]
        }
