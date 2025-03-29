"""Middleware для логирования завершения HTTP-запроса."""

import time
import urllib.parse
from typing import Any, TYPE_CHECKING

from src.app.infrastructure.container import AppContainer

if TYPE_CHECKING:
    from collections.abc import MutableMapping

    from starlette.middleware.base import RequestResponseEndpoint
    from starlette.requests import Request
    from starlette.responses import Response


async def request_logging_middleware(request: 'Request', call_next: 'RequestResponseEndpoint') -> 'Response':
    """Логирует завершение запроса с HTTP-статусом.

    Args:
        request: Входящий HTTP-запрос.
        call_next: Функция вызова следующего middleware/обработчика.

    Returns:
        HTTP-ответ.
    """

    def get_path_with_query_string(scope: 'MutableMapping[str, Any]') -> str:
        """Возвращает полный путь к запрашиваемому ресурсу, включая параметры URL."""
        path_with_query_string = urllib.parse.quote(scope['path'])

        if scope['query_string']:
            query_string = scope['query_string'].decode('ascii')
            path_with_query_string = f'{path_with_query_string}?{query_string}'
        return path_with_query_string

    logger = AppContainer.logger()
    start_time = time.perf_counter_ns()

    try:
        response = await call_next(request)
    except Exception as exc:
        logger.error('unhandled_exception', error=str(exc))
        raise
    finally:
        elapsed_time = int((time.perf_counter_ns() - start_time) / 1_000_000)
        status_code = response.status_code
        host = request.client.host if request.client else None
        url = get_path_with_query_string(request.scope)
        http_method, http_version = request.method, request.scope.get('http_version', '')

        exclude_urls_from_logging: frozenset[str] = frozenset()

        if url not in exclude_urls_from_logging:
            logger.info(
                f'{host} - {http_method} {url} HTTP/{http_version} {status_code}',
                elapsed_time=elapsed_time,
                client={'host': host},
                http={
                    'method': http_method,
                    'status_code': status_code,
                    'version': http_version,
                    'url': url,
                },
            )
    return response
