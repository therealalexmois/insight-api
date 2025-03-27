from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.api
class TestPredictEndpoint:
    @pytest.mark.parametrize(
        'features,expected_prediction',
        [
            ({'age': 20}, 'negative'),
            ({'age': 35}, 'positive'),
            ({'age': 30}, 'negative'),
        ],
    )
    def test_create__ok(
        self,
        sync_api_client: 'TestClient',
        test_user_sync: tuple[str, str],
        features: dict[str, int],
        expected_prediction: str,
    ) -> None:
        """Должен возвращать правильное предсказание, основанное на возрасте."""
        response = sync_api_client.post('/predictions', json=features, auth=test_user_sync)

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {'prediction': expected_prediction}
