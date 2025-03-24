"""Интеграционные тесты для API."""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


@pytest.mark.api
class TestPredict:
    @staticmethod
    @pytest.mark.parametrize(
        'features,expected_prediction',
        [
            ({'age': 20}, 'negative'),
            ({'age': 35}, 'positive'),
            ({'age': 30}, 'negative'),
        ],
    )
    async def test_predict__returns_expected_prediction(
        api_client: 'TestClient',
        test_auth: tuple[str, str],
        features: dict[str, int],
        expected_prediction: str,
    ) -> None:
        """Тест на корректное предсказание модели в зависимости от возраста."""
        response = api_client.post(
            '/predict/',
            json=features,
            auth=test_auth,
        )

        expected_status_code = 200

        assert response.status_code == expected_status_code
        assert response.json() == {'prediction': expected_prediction}


@pytest.mark.api
class TestUsers:
    @staticmethod
    def test_users_me__returns_current_user(
        api_client: 'TestClient',
        test_auth: tuple[str, str],
    ) -> None:
        """Проверяет возврат правильного аутентифицированного пользователя."""
        response = api_client.get('/users/me', auth=test_auth)

        expected_status_code = 200
        expected_age = 25

        assert response.status_code == expected_status_code
        data = response.json()
        assert data['username'] == 'john_doe'
        assert data['email'] == 'john@gmail.de'
        assert data['age'] == expected_age

    @staticmethod
    def test_users_me__unauthorized_without_credentials(api_client: 'TestClient') -> None:
        """Ensure /users/me returns 401 Unauthorized without credentials."""
        response = api_client.get('/users/me')

        epected_status_code = 401

        assert response.status_code == epected_status_code
