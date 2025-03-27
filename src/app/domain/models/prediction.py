"""Доменная модель предсказания."""

from dataclasses import dataclass

from src.app.domain.value_objects.prediction_outcome import PredictionOutcome


@dataclass(frozen=True)
class Prediction:
    """Результат предсказания модели."""

    outcome: PredictionOutcome

    def is_positive(self) -> bool:
        """Проверяет, является ли предсказание положительным.

        Returns:
            True, если результат — положительный.
        """
        return self.outcome == PredictionOutcome.POSITIVE
