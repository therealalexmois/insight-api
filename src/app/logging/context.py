"""Вспомогательные функции для привязки контекста запроса к structlog."""

import uuid
from contextvars import ContextVar
from typing import TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from fastapi import Request

logger = structlog.get_logger()


request_id_ctx: ContextVar[str | None] = ContextVar('request_id', default=None)


def bind_request_context(request: 'Request') -> str:
    """Извлекает или создает X-Request-ID и добавляет контекст запроса в structlog.

    Args:
        request: Объект запроса.

    Returns:
        Уникальный идентификатор запроса (request_id).
    """
    request_id = request.headers.get('X-Request-ID') or _default_generator()
    request_id_ctx.set(request_id)

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
    )
    return request_id


def get_request_id() -> str | None:
    """Возвращает значение идентификатора запроса."""
    return request_id_ctx.get()


def _default_generator() -> str:
    """ФОрмирует уникальный идентификатор."""
    return str(uuid.uuid4())
