"""Логика аутентификации для хэширования паролей и проверки пользователей."""

from typing import cast, TYPE_CHECKING

from passlib.context import CryptContext

from app.exceptions import InvalidCredentialsError

if TYPE_CHECKING:
    from fastapi.security import HTTPBasicCredentials

    from app.models import InternalUser
    from app.repositories.user_repository import UserRepository


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля на его хэшированный аналог.

    Args:
        plain_password: Необработанный пароль, предоставленный пользователем.
        hashed_password: Хешированный пароль, хранящийся в базе данных.

    Returns:
        True, если пароль действителен, False - в противном случае.
    """
    return cast('bool', pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    """Хеширование пароля с помощью bcrypt.

    Args:
        password: Необработанный пароль, предоставленный пользователем.

    Returns:
        Хешированная строка пароля.
    """
    return cast('str', pwd_context.hash(password))


def authenticate_user(credentials: 'HTTPBasicCredentials', user_repository: 'UserRepository') -> 'InternalUser':
    """Аутентификация пользователя с помощью учетных данных HTTP Basic.

    Args:
        credentials: Учетные данные HTTPBasicCredentials, содержащие имя пользователя и пароль.
        user_repository: Репозиторий пользователей для получения данных.

    Returns:
        Объект InternalUser, если аутентификация прошла успешно.

    Raises:
        HTTPException: Если имя пользователя не найдено или пароль неверен.
    """
    username = credentials.username.strip().lower()
    user_data = user_repository.get_by_username(username)

    if user_data is None or not verify_password(credentials.password, user_data.hashed_password):
        raise InvalidCredentialsError()

    return user_data
