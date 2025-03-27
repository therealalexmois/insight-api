"""Middleware для логирования завершения HTTP-запроса."""

from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from starlette.middleware.base import RequestResponseEndpoint
    from starlette.requests import Request
    from starlette.responses import Response


logger = structlog.get_logger()


async def request_logging_middleware(request: 'Request', call_next: 'RequestResponseEndpoint') -> 'Response':
    """Логирует завершение запроса с HTTP-статусом.

    Args:
        request: Входящий HTTP-запрос.
        call_next: Функция вызова следующего middleware/обработчика.

    Returns:
        HTTP-ответ.
    """
    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error('unhandled_exception', error=str(exc))
        raise

    logger.info('request_completed', status_code=response.status_code)
    return response
