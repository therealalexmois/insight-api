"""Маршруты, связанные с пользователями и предсказаниями модели."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth import get_password_hash
from app.config import DEFAULT_SECRET_KEY
from app.db import fake_users_db
from app.dependencies import get_current_user
from app.models import InternalUser, User

router = APIRouter()

current_user_dependency = Depends(get_current_user)


@router.get('/users/me', response_model=User)
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


@router.post('/users/', response_model=User)
def create_user(user: User) -> User:
    """Создает нового пользователя и сохраняет в базе данных.

    Args:
        user: Модель пользователя без пароля.

    Returns:
        Созданный пользователь.
    """
    user_data = user.model_dump()
    user_data['hashed_password'] = get_password_hash(DEFAULT_SECRET_KEY)
    internal_user = InternalUser(**user_data)
    fake_users_db[user.username] = internal_user
    return user
