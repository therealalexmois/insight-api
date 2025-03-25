import asyncio
import logging
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.integration
class TestRequestIdMiddleware:
    @staticmethod
    async def test_unique_per_parallel_request(async_api_client: 'AsyncClient', test_auth: tuple[str, str]) -> None:
        """Каждый параллельный запрос должен иметь уникальный request-id в логах и заголовках."""

        async def send_request() -> str:
            response = await async_api_client.get('/users/me', auth=test_auth)

            expected_response_status = 200
            request_id: str = response.headers.get('x-request-id')

            assert response.status_code == expected_response_status
            assert request_id is not None
            return request_id

        results = await asyncio.gather(*[send_request() for _ in range(10)])

        assert len(results) == len(set(results)), 'Идентификаторы запросов не являются уникальными'

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
            headers={'x-request-id': custom_id},
            auth=test_auth,
        )

        assert response.status_code == expected_status
        assert response.headers['x-request-id'] == custom_id

    @staticmethod
    async def test_logged_in_structlog_context(
        async_api_client: 'AsyncClient',
        test_auth: tuple[str, str],
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Request ID должен появляться в логах после запроса."""
        caplog.set_level(logging.INFO)

        response = await async_api_client.get('/users/me', auth=test_auth)
        request_id = response.headers.get('x-request-id')
        expected_status_code = 200

        assert response.status_code == expected_status_code
        assert request_id is not None

        logs_contain_request_id = any(request_id in message for message in caplog.messages)

        assert logs_contain_request_id, f'request_id {request_id} не найден в логах'

    @staticmethod
    async def test_header_missing_then_autogenerated(
        async_api_client: 'AsyncClient', test_auth: tuple[str, str]
    ) -> None:
        """Если заголовок X-Request-ID отсутствует, middleware должен сгенерировать его."""
        response = await async_api_client.get('/users/me', auth=test_auth)
        request_id = response.headers.get('x-request-id')
        expected_status_code = 200

        assert response.status_code == expected_status_code
        assert request_id is not None
        assert not request_id.startswith('test-custom-id')
