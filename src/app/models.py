"""Pydantic модели для пользовательских данных и запросов/ответов на прогнозирование моделей."""

from pydantic import BaseModel

from app.inference import Prediction  # noqa: TCH001


class User(BaseModel):
    """Публичная модель пользователя, возвращаемая API."""

    username: str
    email: str
    age: int

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'username': 'john_doe',
                    'email': 'john@gmail.de',
                    'age': 25,
                }
            ]
        }
    }


class InternalUser(User):
    """Внутренняя модель пользователя, используемая при аутентификации."""

    hashed_password: str


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
