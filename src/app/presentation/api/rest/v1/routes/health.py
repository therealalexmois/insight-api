"""Маршрут для проверки работоспособности приложения (health check)."""

from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=['system'])


@router.get('health', status_code=HTTPStatus.OK, summary='Health Check')
async def health_check() -> JSONResponse:
    """Возвращает статус работоспособности приложения.

    Returns:
        JSON-ответ с признаком доступности.
    """
    return JSONResponse(content={'status': 'ok'})
