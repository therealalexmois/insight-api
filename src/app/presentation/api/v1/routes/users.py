"""Маршруты, связанные с пользователями."""

from dataclasses import asdict
from http import HTTPStatus
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends

from src.app.domain.models.user import InternalUser
from src.app.infrastructure.config import get_settings
from src.app.presentation.dependencies import get_current_user, get_security_service, get_user_repository
from src.app.presentation.schemas.user import UserCreate, UserResponse

if TYPE_CHECKING:
    from src.app.application.ports.security import SecurityService
    from src.app.domain.repositories.user_repository import UserRepository

settings = get_settings()

router = APIRouter()

current_user_dependency = Depends(get_current_user)
user_repository_dependency = Depends(get_user_repository)
security_service = Depends(get_security_service)


@router.get('users/me', status_code=HTTPStatus.OK, summary='read_current_user')
def read_current_user(current_user: InternalUser = current_user_dependency) -> UserResponse:
    """Возвращает данные текущего аутентифицированного пользователя.

    Args:
        current_user: Текущий пользователь.

    Returns:
        Модель пользователя без пароля.
    """
    return UserResponse.model_validate(current_user, from_attributes=True)


@router.post('users', status_code=HTTPStatus.CREATED, summary='create_user')
def create_user(
    user_data: UserCreate,
    security_service: 'SecurityService' = security_service,
    user_repository: 'UserRepository' = user_repository_dependency,
) -> UserResponse:
    """Создаёт нового пользователя и сохраняет его в репозиторий.

    Получает модель пользователя, хэширует пароль,
    преобразует в InternalUser и сохраняет в репозиторий пользователей.

    Args:
        user_data: Данные о пользователе.
        security_service: Сервис безопасности.
        user_repository: Репозиторий пользователей.

    Returns:
        Созданный пользователь.
    """
    internal_user = InternalUser(
        username=user_data.username,
        email=user_data.email,
        age=user_data.age,
        hashed_password=security_service.hash(user_data.password),
    )

    user_repository.add(internal_user)

    return UserResponse(**asdict(internal_user))
