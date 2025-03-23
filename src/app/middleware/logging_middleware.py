"""Middleware для логирования HTTP-запросов с привязкой контекста и корреляционным ID."""

import uuid
from typing import TYPE_CHECKING

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

if TYPE_CHECKING:
    from starlette.requests import Request
    from starlette.responses import Response

logger = structlog.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware, добавляющий в каждый лог контекст запроса и корреляционный идентификатор."""

    async def dispatch(self, request: 'Request', call_next: 'RequestResponseEndpoint') -> 'Response':
        """Обрабатывает входящий HTTP-запрос, добавляя контекст в логи и корреляционный ID.

        Генерирует или принимает `X-Request-ID`, сохраняет его в контекст `structlog`,
        добавляет метод запроса и путь, логирует завершение запроса и ошибки, и возвращает ответ.

        Args:
            request: Объект входящего HTTP-запроса.
            call_next: Асинхронный обработчик следующего middleware или маршрута.

        Returns:
            Ответ HTTP, дополненный заголовком `X-Request-ID`.

        Raises:
            Любое исключение, возникшее при обработке запроса.
        """
        request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.error(
                'unhandled_exception',
                method=request.method,
                path=request.url.path,
                request_id=request_id,
                error=str(exc),
            )
            raise

        response.headers['X-Request-ID'] = request_id

        logger.info(
            'request_completed',
            status_code=response.status_code,
        )
        return response
