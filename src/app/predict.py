"""Маршруты, связанные с предсказаниями модели."""

from http import HTTPStatus

from fastapi import APIRouter

from app.inference import predict_from_features
from app.schemas.prediction import PredictRequest, PredictResponse

router = APIRouter()


@router.post('/predict/', response_model=PredictResponse, status_code=HTTPStatus.OK, summary='predict')
def predict(request: PredictRequest) -> PredictResponse:
    """Возвращает предсказание модели на основе входных признаков.

    Args:
        request: Входные признаки в виде модели Pydantic.

    Returns:
        Результат предсказания модели.
    """
    prediction = predict_from_features(request.model_dump())
    return PredictResponse(prediction=prediction)
