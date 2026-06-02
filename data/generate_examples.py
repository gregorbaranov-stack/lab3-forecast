"""Генерация дополнительных примеров данных для демонстрации загрузки файла.

Файлы кладутся в data/examples/ и предназначены для ручной загрузки через
кнопку «Загрузить JSON-файл» в интерфейсе. Наборы намеренно отличаются от
демо-данных по умолчанию (другие месяцы, тренды, диапазоны).
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent / "examples"
OUT.mkdir(exist_ok=True)


def dump(name: str, data: list[dict]) -> None:
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  {name}: {len(data)} записей")


def currency(seed, start, days, usd0, eur0, drift_usd, drift_eur, vol) -> list[dict]:
    rnd = random.Random(seed)
    usd, eur = usd0, eur0
    out = []
    for i in range(days):
        day = start + timedelta(days=i)
        usd = round(max(50.0, usd + drift_usd + rnd.uniform(-vol, vol)), 2)
        eur = round(max(55.0, eur + drift_eur + rnd.uniform(-vol, vol)), 2)
        out.append({"date": day.isoformat(), "usd": usd, "eur": eur})
    return out


def temperature(seed, start, days, base0, drift, spread_lo, spread_hi, weather) -> list[dict]:
    rnd = random.Random(seed)
    base = base0
    out = []
    for i in range(days):
        day = start + timedelta(days=i)
        base += drift + rnd.uniform(-1.5, 1.5)
        t_avg = round(base, 1)
        spread = rnd.uniform(spread_lo, spread_hi)
        t_min = round(t_avg - spread / 2, 1)
        t_max = round(t_avg + spread / 2, 1)
        out.append(
            {
                "date": day.isoformat(),
                "t_min": t_min,
                "t_max": t_max,
                "t_avg": t_avg,
                "description": rnd.choice(weather),
            }
        )
    return out


def main() -> None:
    print("Курсы валют (вариант 2):")
    # Июль: рубль постепенно слабеет (курс растёт).
    dump("currency_july_weak_ruble.json", currency(101, date(2026, 7, 1), 31, 92.0, 100.0, 0.25, 0.30, 1.0))
    # Август: рубль укрепляется (курс снижается), другие уровни.
    dump("currency_august_strong_ruble.json", currency(202, date(2026, 8, 1), 31, 95.0, 104.0, -0.30, -0.35, 0.9))

    print("Температура (вариант 3):")
    # Зима: минусовые температуры, большие перепады — проверка цветов и прогноза.
    dump(
        "temperature_winter.json",
        temperature(303, date(2027, 1, 1), 31, -8.0, 0.0, 4.0, 12.0,
                    ["снег", "метель", "ясно", "облачно", "туман"]),
    )
    # Осень: похолодание в течение месяца.
    dump(
        "temperature_autumn.json",
        temperature(404, date(2026, 10, 1), 31, 12.0, -0.25, 3.0, 9.0,
                    ["дождь", "облачно", "туман", "ясно", "переменная облачность"]),
    )


if __name__ == "__main__":
    main()
