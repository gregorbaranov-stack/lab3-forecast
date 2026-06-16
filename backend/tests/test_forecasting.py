"""Проверка соответствия прогноза примеру из методички."""
from app.forecasting import MovingAverageForecaster


def test_moving_average_matches_manual_example():
    """Ряд 60,85,80,92,88,96 при n=5 даёт 88.2, затем 88.84 (как в методичке)."""
    forecaster = MovingAverageForecaster()
    series = [60, 85, 80, 92, 88, 96]
    predictions = forecaster.forecast(series, window=5, horizon=2)
    assert round(predictions[0], 2) == 88.2
    assert round(predictions[1], 2) == 88.84


if __name__ == "__main__":
    test_moving_average_matches_manual_example()
    print("OK: прогноз совпадает с примером методички (88.2, затем 88.84)")
