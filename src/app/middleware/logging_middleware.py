"""Middleware для логирования HTTP-запросов с привязкой контекста и корреляционным ID."""

from typing import TYPE_CHECKING

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.logging.context import bind_request_context

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
        request_id = bind_request_context(request)

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.error(
                'unhandled_exception',
                error=str(exc),
            )
            raise

        response.headers['X-Request-ID'] = request_id

        logger.info(
            'request_completed',
            status_code=response.status_code,
        )
        return response
