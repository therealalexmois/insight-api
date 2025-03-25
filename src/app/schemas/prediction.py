"""Pydantic-схемы для работы с пользователями."""

from pydantic import BaseModel

from src.app.inference import Prediction  # noqa: TCH001


class PredictRequest(BaseModel):
    """Входные признаки для составления прогноза."""

    age: int
    income: float | None = None
    occupation: str | None = None

    model_config = {'json_schema_extra': {'examples': [{'age': 42, 'income': 70000.0, 'occupation': 'engineer'}]}}


class PredictResponse(BaseModel):
    """Модель ответа API, содержащая результат предсказания."""

    prediction: Prediction

    model_config = {'json_schema_extra': {'examples': [{'prediction': 'positive'}]}}
