"""Значения, описывающие результат предсказания модели."""

from enum import Enum


class PredictionOutcome(str, Enum):
    """Возможные исходы предсказания модели."""

    POSITIVE = 'positive'
    NEGATIVE = 'negative'


PREDICTION_AGE_THRESHOLD = 30
