import asyncio
import logging
from typing import cast, Final, TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from httpx import AsyncClient


X_REQUEST_ID_HEADER: Final[str] = 'x-request-id'
TEST_CUSTOM_ID_PREFIX: Final[str] = 'test-custom-id'


@pytest.mark.asyncio
@pytest.mark.integration
class TestRequestIdMiddleware:
    @staticmethod
    async def test_request_id__returns_header_and_status_200(
        async_api_client: 'AsyncClient', test_auth: tuple[str, str]
    ) -> None:
        """Middleware должен возвращать заголовок X-Request-ID и статус 200."""
        response = await async_api_client.get('/users/me', auth=test_auth)

        request_id: str = response.headers.get(X_REQUEST_ID_HEADER)
        expected_response_status = 200

        assert response.status_code == expected_response_status
        assert request_id is not None

    @staticmethod
    @pytest.mark.parametrize(
        'custom_id,expected_status',
        [
            ('test-custom-id-123', 200),
            ('another-id-456', 200),
        ],
    )
    async def test_request_id__uses_custom_header(
        async_api_client: 'AsyncClient',
        test_auth: tuple[str, str],
        custom_id: str,
        expected_status: int,
    ) -> None:
        """Проверяет, что клиентский X-Request-ID используется в middleware."""
        response = await async_api_client.get(
            '/users/me',
            headers={X_REQUEST_ID_HEADER: custom_id},
            auth=test_auth,
        )

        assert response.status_code == expected_status
        assert response.headers[X_REQUEST_ID_HEADER] == custom_id

    @staticmethod
    async def test_header_missing_then_autogenerated(
        async_api_client: 'AsyncClient', test_auth: tuple[str, str]
    ) -> None:
        """Если заголовок X-Request-ID отсутствует, middleware должен сгенерировать его."""
        response = await async_api_client.get('/users/me', auth=test_auth)
        request_id: str = response.headers.get(X_REQUEST_ID_HEADER)
        expected_status_code = 200

        assert response.status_code == expected_status_code
        assert request_id is not None
        assert not request_id.startswith(TEST_CUSTOM_ID_PREFIX)

    @staticmethod
    async def test_logged_in_structlog_context(
        async_api_client: 'AsyncClient',
        test_auth: tuple[str, str],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Request ID должен появляться в логах после запроса."""
        caplog.set_level(logging.INFO)

        response = await async_api_client.get('/users/me', auth=test_auth)
        request_id: str = response.headers.get(X_REQUEST_ID_HEADER)
        expected_status_code = 200

        assert response.status_code == expected_status_code
        assert request_id is not None

        logs_contain_request_id = any(request_id in message for message in caplog.messages)

        assert logs_contain_request_id, f'request_id {request_id} не найден в логах'

    @staticmethod
    async def test_request_id__unique_per_parallel_request(
        async_api_client: 'AsyncClient', test_auth: tuple[str, str]
    ) -> None:
        """Каждый параллельный запрос должен иметь уникальный X-Request-ID."""

        async def send_request() -> str:
            response = await async_api_client.get('/users/me', auth=test_auth)
            return cast('str', response.headers.get(X_REQUEST_ID_HEADER))

        concurrent_requests = 10
        results = await asyncio.gather(*[send_request() for _ in range(concurrent_requests)])

        assert len(results) == len(set(results)), 'Идентификаторы запросов не являются уникальными'
