"""Сервис для выполнения предсказаний модели на основе входных признаков."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

from src.app.domain.value_objects.prediction_outcome import PREDICTION_AGE_THRESHOLD, PredictionOutcome


def predict_from_features(features: 'Mapping[str, int | float | str | None]') -> PredictionOutcome:
    """Моделирует логику предсказания на основе входных признаков.

    Args:
        features: Словарь входных признаков.

    Returns:
        Значение прогноза, представляющее выход модели.
    """
    age_raw = features.get('age', 0)

    if isinstance(age_raw, (int | float)):
        return PredictionOutcome.POSITIVE if age_raw > PREDICTION_AGE_THRESHOLD else PredictionOutcome.NEGATIVE

    return PredictionOutcome.NEGATIVE
