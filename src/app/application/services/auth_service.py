"""Сервис для аутентификации пользователей."""

from typing import TYPE_CHECKING

from src.app.domain.exceptions import InvalidCredentialsError
from src.app.infrastructure.container import AppContainer

if TYPE_CHECKING:
    from src.app.domain.models.user import InternalUser
    from src.app.domain.repositories.user_repository import UserRepository


def authenticate_user(username: str, password: str, user_repository: 'UserRepository') -> 'InternalUser':
    """Аутентифицирует пользователя по имени и паролю.

    Args:
        username: Имя пользователя.
        password: Пароль.
        user_repository: Репозиторий пользователей.

    Returns:
        Пользователь, если аутентификация прошла успешно.

    Raises:
        InvalidCredentialsError: Если пользователь не найден или пароль неверен.
    """
    user: InternalUser | None = user_repository.get_by_username(username.strip().lower())
    password_hasher = AppContainer.security_service()

    if user is None or not password_hasher.verify(password, user.hashed_password):
        raise InvalidCredentialsError()

    return user
