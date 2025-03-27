"""Схемы Pydantic для работы с предсказаниями."""

from pydantic import BaseModel

from src.app.domain.value_objects.prediction_outcome import PredictionOutcome  # noqa: TCH001


class PredictRequest(BaseModel):
    """Схема входных признаков для предсказания."""

    age: int
    income: float | None = None
    occupation: str | None = None

    model_config = {
        'json_schema_extra': {
            'examples': [
                {'age': 42, 'income': 70000.0, 'occupation': 'engineer'},
            ]
        }
    }


class PredictResponse(BaseModel):
    """Схема ответа с результатом предсказания."""

    prediction: PredictionOutcome

    model_config = {
        'json_schema_extra': {
            'examples': [
                {'prediction': 'positive'},
            ]
        }
    }
