"""Зависимости FastAPI для повторного использования логики."""

from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.app.auth import authenticate_user
from src.app.container import AppContainer

if TYPE_CHECKING:
    from src.app.repositories.user_repository import UserRepository
    from src.app.schemas.user import InternalUser

security = HTTPBasic()

credentials: HTTPBasicCredentials = Depends(security)


def get_user_repository() -> 'UserRepository':
    """Возвращает экземпляр репозитория пользователей."""
    return AppContainer.user_repository()


user_repository_dependency = Depends(get_user_repository)


def get_current_user(
    credentials: HTTPBasicCredentials = credentials, user_repository: 'UserRepository' = user_repository_dependency
) -> 'InternalUser':
    """Зависимость для получения текущего аутентифицированного пользователя.

    Args:
        credentials: Учетные данные HTTP Basic.
        user_repository: Репозиторий пользователей.

    Returns:
        Внутренняя модель пользователя, если аутентификация прошла успешно.
    """
    return authenticate_user(credentials, user_repository)
