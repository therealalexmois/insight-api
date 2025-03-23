"""Зависимости FastAPI для повторного использования логики."""

from typing import TYPE_CHECKING

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.auth import authenticate_user

if TYPE_CHECKING:
    from app.models import InternalUser

security = HTTPBasic()
credentials: HTTPBasicCredentials = Depends(security)


def get_current_user(credentials: HTTPBasicCredentials = credentials) -> 'InternalUser':
    """Зависимость для получения текущего аутентифицированного пользователя.

    Args:
        credentials: Учетные данные HTTP Basic.

    Returns:
        Внутренняя модель пользователя, если аутентификация прошла успешно.
    """
    return authenticate_user(credentials)
