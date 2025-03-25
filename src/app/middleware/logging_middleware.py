"""Middleware для логирования HTTP-запросов с привязкой контекста и корреляционным ID."""

from typing import TYPE_CHECKING

import structlog

from app.logging.context import bind_request_context

if TYPE_CHECKING:
    from starlette.middleware.base import RequestResponseEndpoint
    from starlette.requests import Request
    from starlette.responses import Response

logger = structlog.get_logger()


async def logging_middleware(request: 'Request', call_next: 'RequestResponseEndpoint') -> 'Response':
    """Middleware, добавляющий контекст запроса и X-Request-ID в structlog.

    Args:
        request: Объект входящего HTTP-запроса.
        call_next: Функция вызова следующего обработчика.

    Returns:
        Ответ HTTP с заголовком X-Request-ID.
    """
    request_id = bind_request_context(request)

    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error('unhandled_exception', error=str(exc))
        raise

    response.headers['X-Request-ID'] = request_id

    logger.info('request_completed', status_code=response.status_code)
    return response
