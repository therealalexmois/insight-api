"""Вспомогательные функции для привязки контекста запроса к structlog."""

import uuid
from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from starlette.requests import Request

logger = structlog.get_logger()


def bind_request_context(request: 'Request') -> str:
    """Извлекает или создает X-Request-ID и добавляет контекст запроса в structlog.

    Args:
        request: Объект запроса.

    Returns:
        Уникальный идентификатор запроса (request_id).
    """
    request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
    )
    return request_id
