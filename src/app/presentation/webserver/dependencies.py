"""Зависимости FastAPI для повторного использования логики."""

from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.app.application.services.auth_service import authenticate_user
from src.app.infrastructure.container import AppContainer

if TYPE_CHECKING:
    from src.app.application.ports.security import SecurityService
    from src.app.domain.models.user import InternalUser
    from src.app.domain.repositories.user_repository import UserRepository

security = HTTPBasic()

credentials: HTTPBasicCredentials = Depends(security)


def get_user_repository() -> 'UserRepository':
    """Возвращает экземпляр репозитория пользователей."""
    return AppContainer.user_repository()


def get_security_service() -> 'SecurityService':
    """Возвращает экземпляр сервиса безопасности."""
    return AppContainer.security_service()


user_repository_dependency = Depends(get_user_repository)
security_service_dependency = Depends(get_security_service)


def get_current_user(
    credentials: HTTPBasicCredentials = credentials,
    security_service: 'SecurityService' = security_service_dependency,
    user_repository: 'UserRepository' = user_repository_dependency,
) -> 'InternalUser':
    """Зависимость для получения текущего аутентифицированного пользователя.

    Args:
        credentials: Учетные данные HTTP Basic.
        security_service: Сервис безопасности.
        user_repository: Репозиторий пользователей.

    Returns:
        Внутренняя модель пользователя, если аутентификация прошла успешно.
    """
    return authenticate_user(credentials.username, credentials.password, security_service, user_repository)
