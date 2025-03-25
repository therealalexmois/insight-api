"""Интеграционные тесты для API."""

from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


@pytest.mark.api
class TestUsersMeEndpoint:
    @staticmethod
    def test_read_current_user__ok(api_client: 'TestClient', test_auth: tuple[str, str]) -> None:
        """Должен возвращать информацию о текущем аутентифицированном пользователе."""
        response = api_client.get('/users/me', auth=test_auth)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            'username': 'john_doe',
            'email': 'john@gmail.de',
            'age': 25,
        }

    @staticmethod
    def test_read_current_user__unauthorized(api_client: 'TestClient') -> None:
        """Должен возвращать 401 Unauthorized, если не предоставлены учетные данные."""
        response = api_client.get('/users/me')

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Not authenticated'}

    @staticmethod
    @pytest.mark.parametrize(
        'auth',
        [
            ('invalid_user', 'dev_secret'),
            ('john_doe', 'wrong_secret'),
        ],
    )
    def test_read_current_user__invalid_credentials(api_client: 'TestClient', auth: tuple[str, str]) -> None:
        """Должен возвращать 401 Unauthorized для недействительных учетных данных."""
        response = api_client.get('/users/me', auth=auth)

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Incorrect username or password'}


@pytest.mark.api
class TestPredictEndpoint:
    @staticmethod
    @pytest.mark.parametrize(
        'features,expected_prediction',
        [
            ({'age': 20}, 'negative'),
            ({'age': 35}, 'positive'),
            ({'age': 30}, 'negative'),
        ],
    )
    def test_create__ok(
        api_client: 'TestClient',
        test_auth: tuple[str, str],
        features: dict[str, int],
        expected_prediction: str,
    ) -> None:
        """Должен возвращать правильное предсказание, основанное на возрасте."""
        response = api_client.post('/predict/', json=features, auth=test_auth)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'prediction': expected_prediction}
