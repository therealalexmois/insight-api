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
        [
            ('invalid_user', 'dev_secret'),
            ('john_doe', 'wrong_secret'),
        ],
    )
    @staticmethod
    def test_read_current_user__invalid_credentials(sync_api_client: 'TestClient') -> None:
        """Должен возвращать 401 Unauthorized для недействительных учетных данных."""
        response = sync_api_client.get('/users/me', auth=('invalid', 'invalid'))

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Incorrect username or password'}


@pytest.mark.integration
@pytest.mark.api
class TestCreateUserEndpoint:
    @staticmethod
    def test_create_user__ok(sync_api_client: 'TestClient') -> None:
        """Должен успешно создать нового пользователя и вернуть 201."""
        user_data = {
            'username': 'new_user',
            'email': 'new_user@example.com',
            'age': 28,
            'password': 'secure12345',
        }

        response = sync_api_client.post('/users', json=user_data)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            'username': user_data['username'],
            'email': user_data['email'],
            'age': user_data['age'],
        }

    @staticmethod
    def test_create_user__invalid_email(sync_api_client: 'TestClient') -> None:
        """Должен вернуть 422, если email некорректный."""
        bad_data = {
            'username': 'new_user',
            'email': 'not-an-email',
            'age': 28,
            'password': 'secure12345',
        }

        response = sync_api_client.post('/users', json=bad_data)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    @staticmethod
    def test_create_user__short_password(sync_api_client: 'TestClient') -> None:
        """Должен вернуть 422, если пароль слишком короткий."""
        bad_data = {
            'username': 'short_pass_user',
            'email': 'short@pass.com',
            'age': 22,
            'password': '123',
        }

        response = sync_api_client.post('/users', json=bad_data)

        assert response.status_code == HTTPStatus.BAD_REQUEST

    @staticmethod
    def test_create_user__duplicate_username(sync_api_client: 'TestClient') -> None:
        """Должен вернуть 409, если пользователь уже существует."""
        username = 'duplicate_user'
        user_data = {
            'username': username,
            'email': 'dupe@example.com',
            'age': 30,
            'password': 'securepassword123',
        }

        first_response = sync_api_client.post('/users', json=user_data)
        assert first_response.status_code == HTTPStatus.CREATED

        second_response = sync_api_client.post('/users', json=user_data)
        assert second_response.status_code == HTTPStatus.CONFLICT
        assert second_response.json()['detail'] == f'User "{username}" already exists'
