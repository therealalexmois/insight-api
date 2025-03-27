"""Маршруты, связанные с пользователями."""

from dataclasses import asdict
from http import HTTPStatus
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends

from src.app.domain.models.user import InternalUser
from src.app.infrastructure.config import get_settings
from src.app.infrastructure.container import AppContainer
from src.app.presentation.dependencies import get_current_user, get_user_repository
from src.app.presentation.schemas.user import UserCreate, UserResponse

if TYPE_CHECKING:
    from src.app.domain.repositories.user_repository import UserRepository

settings = get_settings()

router = APIRouter()

current_user_dependency = Depends(get_current_user)
user_repository_dependency = Depends(get_user_repository)


@router.get('/users/me', status_code=HTTPStatus.OK, summary='read_current_user')
def read_current_user(current_user: InternalUser = current_user_dependency) -> UserResponse:
    """Возвращает данные текущего аутентифицированного пользователя.

    Args:
        current_user: Текущий пользователь.

    Returns:
        Модель пользователя без пароля.
    """
    return UserResponse.model_validate(current_user)


@router.post('/users', status_code=HTTPStatus.CREATED, summary='create_user')
def create_user(user_data: UserCreate, user_repository: 'UserRepository' = user_repository_dependency) -> UserResponse:
    """Создаёт нового пользователя и сохраняет его в репозиторий.

    Получает модель пользователя, хэширует пароль,
    преобразует в InternalUser и сохраняет в репозиторий пользователей.

    Args:
        user_data: Данные о пользователе.
        user_repository: Репозиторий пользователей.

    Returns:
        Созданный пользователь.
    """
    password_hasher = AppContainer.security_service()
    internal_user = InternalUser(
        username=user_data.username,
        email=user_data.email,
        age=user_data.age,
        hashed_password=password_hasher.hash(user_data.password),
    )

    user_repository.add(internal_user)

    return UserResponse(**asdict(internal_user))
