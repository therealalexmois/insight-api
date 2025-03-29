"""Зависимости FastAPI для повторного использования логики."""

from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer

from src.app.application.services.auth_service import authenticate_user
from src.app.infrastructure.container import AppContainer

if TYPE_CHECKING:
    from src.app.application.ports.security.password_hasher import PasswordHasher
    from src.app.domain.models.user import InternalUser
    from src.app.domain.repositories.user_repository import UserRepository

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/token')

credentials: HTTPBasicCredentials = Depends(security)


def get_user_repository() -> 'UserRepository':
    """Возвращает экземпляр репозитория пользователей."""
    return AppContainer.user_repository()


def get_password_hasher() -> 'PasswordHasher':
    """Возвращает экземпляр сервиса безопасности."""
    return AppContainer.password_hasher()


user_repository_dependency = Depends(get_user_repository)
password_hasher_dependency = Depends(get_password_hasher)


def get_current_user(
    credentials: HTTPBasicCredentials = credentials,
    password_hasher: 'PasswordHasher' = password_hasher_dependency,
    user_repository: 'UserRepository' = user_repository_dependency,
) -> 'InternalUser':
    """Зависимость для получения текущего аутентифицированного пользователя.

    Args:
        credentials: Учетные данные HTTP Basic.
        password_hasher: Сервиса хеширования паролей.
        user_repository: Репозиторий пользователей.

    Returns:
        Внутренняя модель пользователя, если аутентификация прошла успешно.
    """
    return authenticate_user(credentials.username, credentials.password, password_hasher, user_repository)
