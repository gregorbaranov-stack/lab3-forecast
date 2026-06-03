"""Pydantic-модели записей данных.

Демонстрируют инкапсуляцию: внутреннее представление одного дня данных
скрыто за моделью с валидацией, недопустимые значения отсекаются на входе.
"""
from __future__ import annotations

from pydantic import BaseModel, field_validator, model_validator


class CurrencyRecord(BaseModel):
    """Курс рубля к двум валютам за один день (рублей за единицу валюты)."""

    date: str
    usd: float  # рублей за 1 доллар США
    eur: float  # рублей за 1 евро

    @field_validator("usd", "eur")
    @classmethod
    def _positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Курс валюты должен быть положительным")
        return value


class TemperatureRecord(BaseModel):
    """Температура в городе за один день."""

    date: str
    t_min: float
    t_max: float
    t_avg: float
    description: str = ""

    @model_validator(mode="after")
    def _check_order(self) -> "TemperatureRecord":
        if not (self.t_min <= self.t_avg <= self.t_max):
            raise ValueError("Должно выполняться t_min ≤ t_avg ≤ t_max")
        return self
