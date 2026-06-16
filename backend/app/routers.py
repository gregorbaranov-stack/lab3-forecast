"""REST API: список вариантов и анализ данных варианта."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .forecasting import MovingAverageForecaster
from .services import AnalysisService, DatasetFactory

router = APIRouter(prefix="/api")

# Сервис собирается с конкретной стратегией прогноза (внедрение зависимости).
_service = AnalysisService(MovingAverageForecaster())


class Period(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None


class AnalyzeRequest(BaseModel):
    records: Optional[list[dict]] = None  # если не передано — берётся демо-набор
    n: int = 5            # размер окна скользящей средней
    horizon: int = 7      # сколько периодов прогнозировать
    period: Optional[Period] = None


@router.get("/datasets")
def list_datasets() -> list[dict]:
    """Список доступных вариантов (для навигации интерфейса)."""
    return DatasetFactory.available()


@router.post("/{variant}/analyze")
def analyze(variant: str, request: AnalyzeRequest) -> dict:
    """Анализ данных варианта: таблица, ряды, статистика и прогноз."""
    try:
        return _service.analyze(
            variant=variant,
            raw=request.records,
            window=request.n,
            horizon=request.horizon,
            period=request.period.model_dump() if request.period else None,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
