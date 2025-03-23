"""Логика аутентификации для хэширования паролей и проверки пользователей."""

from typing import cast, TYPE_CHECKING

from passlib.context import CryptContext

from app.exceptions import InvalidCredentialsError, UserNotFoundError

if TYPE_CHECKING:
    from fastapi.security import HTTPBasicCredentials

    from app.models import InternalUser


from app.db import fake_users_db

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


def authenticate_user(credentials: 'HTTPBasicCredentials') -> 'InternalUser':
    """Аутентификация пользователя с помощью учетных данных HTTP Basic.

    Args:
        credentials: Учетные данные HTTPBasicCredentials, содержащие имя пользователя и пароль.

    Returns:
        Объект InternalUser, если аутентификация прошла успешно.

    Raises:
        HTTPException: Если имя пользователя не найдено или пароль неверен.
    """
    user_data = fake_users_db.get(credentials.username)

    if user_data is None:
        raise UserNotFoundError()

    if not verify_password(credentials.password, user_data.hashed_password):
        raise InvalidCredentialsError()

    return user_data
