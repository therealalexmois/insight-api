from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.api
class TestUsersMeEndpoint:
    @staticmethod
    def test_read_current_user__ok(sync_api_client: 'TestClient', test_user_sync: tuple[str, str]) -> None:
        """Должен возвращать информацию о текущем аутентифицированном пользователе."""
        username, _ = test_user_sync
        response = sync_api_client.get('/users/me', auth=test_user_sync)

        expected_user = {
            'username': username,
            'email': f'{username}@example.com',
            'age': 30,
        }

        assert response.status_code == HTTPStatus.OK
        assert response.json() == expected_user

    @staticmethod
    def test_read_current_user__unauthorized(sync_api_client: 'TestClient') -> None:
        """Должен возвращать 401 Unauthorized, если не предоставлены учетные данные."""
        response = sync_api_client.get('/users/me')

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Not authenticated'}

    @pytest.mark.parametrize(
        'auth',
        [('invalid_user', 'dev_secret'), ('john_doe', 'wrong_secret')],
    )
    @staticmethod
    def test_read_current_user__invalid_credentials(
        sync_api_client: 'TestClient', test_user_sync: tuple[str, str]
    ) -> None:
        """Должен возвращать 401 Unauthorized для недействительных учетных данных."""
        response = sync_api_client.get('/users/me', auth=test_user_sync)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Incorrect username or password'}
