"""Общие фикстуры pytest для интеграционного тестирования."""

from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient

from src.app.main import create_app

if TYPE_CHECKING:
    from collections.abc import Generator

    from fastapi import FastAPI


@pytest.fixture
def fastapi_app() -> 'FastAPI':
    """Предоставляет экземпляр приложения FastAPI для тестирования."""
    return create_app()


@pytest.fixture
def api_client(fastapi_app: 'FastAPI') -> 'Generator[TestClient]':
    """Предоставляет синхронный экземпляр TestClient для запросов API."""
    with TestClient(fastapi_app) as client:
        yield client


DEFAULT_TEST_USERNAME = 'john_doe'
DEFAULT_TEST_SECRET_KEY = 'dev_secret'


@pytest.fixture()
def test_auth() -> tuple[str, str]:
    """Предоставляет учетные данные аутентификации по умолчанию для тестирования."""
    return DEFAULT_TEST_USERNAME, DEFAULT_TEST_SECRET_KEY
