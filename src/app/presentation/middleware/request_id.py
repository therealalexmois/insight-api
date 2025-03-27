"""Middleware для привязки X-Request-ID и установки контекста логгера."""

from typing import TYPE_CHECKING

from src.app.infrastructure.logger.context import bind_logging_context, DEFAULT_REQUEST_ID_HEADER, extract_request_id

if TYPE_CHECKING:
    from starlette.middleware.base import RequestResponseEndpoint
    from starlette.requests import Request
    from starlette.responses import Response


async def request_id_middleware(request: 'Request', call_next: 'RequestResponseEndpoint') -> 'Response':
    """Добавляет X-Request-ID и устанавливает контекст structlog.

    Args:
        request: Входящий HTTP-запрос.
        call_next: Функция вызова следующего middleware/обработчика.

    Returns:
        HTTP-ответ с заголовком X-Request-ID.
    """
    request_id = extract_request_id(request)
    bind_logging_context(request_id, request)

    response = await call_next(request)
    response.headers[DEFAULT_REQUEST_ID_HEADER] = request_id
    return response
