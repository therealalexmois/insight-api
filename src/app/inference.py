"""Модуль-заглушка для логики вывода модели."""

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping


AGE_THRESHOLD = 30


class Prediction(str, Enum):
    """Возможные результаты прогнозирования."""

    POSITIVE = 'positive'
    NEGATIVE = 'negative'


def predict_from_features(features: 'Mapping[str, int | float | str | None]') -> Prediction:
    """Моделирует логику предсказания на основе входных признаков.

    Args:
        features: Словарь входных признаков.

    Returns:
        Значение прогноза, представляющее выход модели.
    """
    age_raw = features.get('age', 0)
    if isinstance(age_raw, (int | float)):
        return Prediction.POSITIVE if age_raw > AGE_THRESHOLD else Prediction.NEGATIVE

    return Prediction.NEGATIVE
