from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from httpx import AsyncClient


@pytest.mark.critical
@pytest.mark.asyncio
class TestMain:
    async def test_app_startup__returns_200(self, async_api_client: 'AsyncClient') -> None:
        """Критический тест: приложение должно успешно запускаться и обрабатывать запросы."""
        response = await async_api_client.get('/health')

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'status': 'ok'}
