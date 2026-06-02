"""Генерация синтетических данных за 30 дней (детерминированно, seed=42).

Задание разрешает использовать случайно сгенерированные данные. Наборы
сохраняются в data/ и дублируются в frontend/public/sample/ для демо-режима.
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

START = date(2026, 6, 1)
DAYS = 30
HERE = Path(__file__).resolve().parent


def generate_currency() -> list[dict]:
    """Курс рубля к USD и EUR с реалистичными дневными колебаниями."""
    usd, eur = 92.0, 100.0
    records = []
    for i in range(DAYS):
        day = START + timedelta(days=i)
        usd = round(max(80.0, usd + random.uniform(-1.2, 1.2)), 2)
        eur = round(max(88.0, eur + random.uniform(-1.4, 1.4)), 2)
        records.append({"date": day.isoformat(), "usd": usd, "eur": eur})
    return records


WEATHER = ["ясно", "облачно", "переменная облачность", "дождь", "гроза", "туман"]


def generate_temperature() -> list[dict]:
    """Температура с согласованными min <= avg <= max."""
    base = 18.0
    records = []
    for i in range(DAYS):
        day = START + timedelta(days=i)
        base += random.uniform(-1.5, 1.5)
        t_avg = round(base, 1)
        spread = random.uniform(3.0, 9.0)
        t_min = round(t_avg - spread / 2, 1)
        t_max = round(t_avg + spread / 2, 1)
        records.append(
            {
                "date": day.isoformat(),
                "t_min": t_min,
                "t_max": t_max,
                "t_avg": t_avg,
                "description": random.choice(WEATHER),
            }
        )
    return records


def _dump(path: Path, data: list[dict]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    currency = generate_currency()
    temperature = generate_temperature()

    _dump(HERE / "currency_month.json", currency)
    _dump(HERE / "temperature_month.json", temperature)

    sample_dir = HERE.parent / "frontend" / "public" / "sample"
    sample_dir.mkdir(parents=True, exist_ok=True)
    _dump(sample_dir / "currency_month.json", currency)
    _dump(sample_dir / "temperature_month.json", temperature)

    print(f"Сгенерировано: {len(currency)} дней курсов, {len(temperature)} дней температуры")


if __name__ == "__main__":
    main()
