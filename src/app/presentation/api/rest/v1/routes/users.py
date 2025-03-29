"""Маршруты, связанные с пользователями."""

from dataclasses import asdict
from http import HTTPStatus

from fastapi import APIRouter

from src.app.domain.models.user import InternalUser
from src.app.infrastructure.config import get_settings
from src.app.infrastructure.presenters.user_presenter import UserPresenter
from src.app.presentation.schemas.user import UserCreate, UserResponse
from src.app.presentation.webserver.dependencies import (  # noqa: TCH001
    CurrentUserHTTPBasicDep,
    HasherDep,
    UserRepoDep,
)

settings = get_settings()

router = APIRouter(tags=['users'])


@router.get('users/me', status_code=HTTPStatus.OK, summary='read_current_user')
def read_current_user(current_user: CurrentUserHTTPBasicDep) -> UserResponse:
    """Возвращает данные текущего аутентифицированного пользователя.

    Args:
        current_user: Текущий пользователь.

    Returns:
        Модель пользователя без пароля.
    """
    return UserPresenter.to_response(current_user)


@router.post('users', status_code=HTTPStatus.CREATED, summary='create_user')
def create_user(
    user_data: UserCreate,
    password_hasher: HasherDep,
    user_repository: UserRepoDep,
) -> UserResponse:
    """Создаёт нового пользователя и сохраняет его в репозиторий.

    Получает модель пользователя, хэширует пароль,
    преобразует в InternalUser и сохраняет в репозиторий пользователей.

    Args:
        user_data: Данные о пользователе.
        password_hasher: Сервиса хеширования паролей.
        user_repository: Репозиторий пользователей.

    Returns:
        Созданный пользователь.
    """
    internal_user = InternalUser(
        username=user_data.username,
        email=user_data.email,
        age=user_data.age,
        hashed_password=password_hasher.hash(user_data.password),
        role=user_data.role,
    )

    user_repository.add(internal_user)

    return UserResponse(**asdict(internal_user))
