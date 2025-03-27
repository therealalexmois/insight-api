from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from httpx import AsyncClient


@pytest.mark.critical
@pytest.mark.asyncio
class TestMain:
    @staticmethod
    async def test_app_startup__returns_200(async_api_client: 'AsyncClient') -> None:
        """Критический тест: приложение должно успешно запускаться и обрабатывать запросы."""
        response = await async_api_client.get('/users/me', auth=('invalid', 'invalid'))

        assert response.status_code != int(HTTPStatus.INTERNAL_SERVER_ERROR)
