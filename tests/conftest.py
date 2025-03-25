"""Общие фикстуры pytest для интеграционного тестирования."""

import uuid
from http import HTTPStatus
from typing import TYPE_CHECKING

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.app.main import create_app

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Generator

    from fastapi import FastAPI


@pytest.fixture
def fastapi_app() -> 'FastAPI':
    """Предоставляет экземпляр приложения FastAPI для тестирования."""
    return create_app()


@pytest.fixture
def sync_api_client(fastapi_app: 'FastAPI') -> 'Generator[TestClient]':
    """Клиент Sync API - для базовых интеграционных тестов."""
    with TestClient(fastapi_app) as client:
        yield client


@pytest.fixture
async def async_api_client(fastapi_app: 'FastAPI') -> 'AsyncGenerator[AsyncClient]':
    """Клиент Async API - для параллельных/асинхронных интеграционных тестов."""
    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url='http://test') as client:
        yield client


@pytest.fixture()
def test_user_sync(sync_api_client: TestClient) -> tuple[str, str]:
    """Создает пользователя через синхронный API-клиент."""
    username = f'user_{uuid.uuid4().hex[:8]}'
    password = uuid.uuid4().hex[:12]

    response = sync_api_client.post(
        '/users/',
        json={
            'username': username,
            'email': f'{username}@example.com',
            'age': 30,
            'password': password,
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    return username, password


@pytest.fixture()
async def test_user_async(async_api_client: AsyncClient) -> tuple[str, str]:
    """Создает пользователя через асинхронный API-клиент."""
    username = f'user_{uuid.uuid4().hex[:8]}'
    password = uuid.uuid4().hex[:12]

    response = await async_api_client.post(
        '/users/',
        json={
            'username': username,
            'email': f'{username}@example.com',
            'age': 30,
            'password': password,
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    return username, password
