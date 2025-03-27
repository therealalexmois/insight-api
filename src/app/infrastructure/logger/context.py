"""Вспомогательные функции для привязки контекста запроса к structlog."""

import uuid
from contextvars import ContextVar
from typing import Final, TYPE_CHECKING

import structlog

if TYPE_CHECKING:
    from fastapi import Request

request_id_ctx: ContextVar[str | None] = ContextVar('request_id', default=None)


DEFAULT_REQUEST_ID_HEADER: Final[str] = 'X-Request-ID'


def extract_request_id(request: 'Request') -> str:
    """Извлекает X-Request-ID или генерирует новый."""
    return request.headers.get(DEFAULT_REQUEST_ID_HEADER) or _default_generator()


def bind_logging_context(request_id: str, request: 'Request') -> None:
    """Добавляет X-Request-ID в контекст запроса structlog.

    Args:
        request_id: Идентификатор запроса.
        request: Объект запроса.
    """
    request_id_ctx.set(request_id)

    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
    )


def get_request_id() -> str | None:
    """Возвращает значение идентификатора запроса."""
    return request_id_ctx.get()


def _default_generator() -> str:
    """Формирует уникальный идентификатор."""
    return str(uuid.uuid4())
