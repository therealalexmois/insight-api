"""Маршруты, связанные с пользователями и предсказаниями модели."""

from http import HTTPStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Annotated

    from app.repositories.user_repository import UserRepository

from fastapi import APIRouter, Depends

from app.config import get_settings
from app.dependencies import get_current_user, get_user_repository
from app.models import InternalUser, User
from app.security import get_password_hash

settings = get_settings()

router = APIRouter()

current_user_dependency = Depends(get_current_user)


@router.get('/users/me', response_model=User, status_code=HTTPStatus.OK, summary='read_current_user')
def read_current_user(
    current_user: 'Annotated[InternalUser, Depends(get_current_user)]' = current_user_dependency,
) -> User:
    """Возвращает данные текущего аутентифицированного пользователя.

    Args:
        current_user: Полученный через Depends пользователь.

    Returns:
        Модель пользователя без пароля.
    """
    return User(**current_user.model_dump())


@router.post('/users/', response_model=User, status_code=HTTPStatus.CREATED, summary='create_user')
def create_user(user: User, user_repository: 'Annotated[UserRepository, Depends(get_user_repository)]') -> User:
    """Создает нового пользователя и сохраняет его в репозиторий.

    Получает модель пользователя без пароля, хэширует пароль,
    преобразует в InternalUser и сохраняет в репозиторий пользователей.

    Args:
        user: Модель пользователя без пароля.
        user_repository: Репозиторий пользователей, полученный через Depends.

    Returns:
        Созданный пользователь.
    """
    user_data = user.model_dump()
    user_data['hashed_password'] = get_password_hash(settings.app.secret_key.get_secret_value())
    internal_user = InternalUser(**user_data)
    user_repository.add(internal_user)
    return user
