"""Сервис для аутентификации пользователей."""

from typing import TYPE_CHECKING

from src.app.domain.exceptions import InvalidCredentialsError

if TYPE_CHECKING:
    from src.app.application.ports.security.password_hasher import PasswordHasher
    from src.app.domain.models.user import InternalUser
    from src.app.domain.repositories.user_repository import UserRepository


def verify_password(password: str, hashed_password: str, password_hasher: 'PasswordHasher') -> None:
    """Проверяет корректность пароля по хешу.

    Args:
        password: Открытый пароль.
        hashed_password: Хеш пароля.
        password_hasher: Сервис хеширования паролей.

    Raises:
        InvalidCredentialsError: Если пароль не совпадает.
    """
    if not password_hasher.verify(password, hashed_password):
        raise InvalidCredentialsError()


def resolve_current_user(
    username: str,
    user_repository: 'UserRepository',
) -> 'InternalUser':
    """Возвращает пользователя по имени.

    Args:
        username: Имя пользователя.
        user_repository: Репозиторий пользователей.

    Returns:
        Пользователь.

    Raises:
        InvalidCredentialsError: Если пользователь не найден.
    """
    user: InternalUser | None = user_repository.get_by_username(username.strip().lower())

    if not user:
        raise InvalidCredentialsError()

    return user
