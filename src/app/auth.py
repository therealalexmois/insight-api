"""Логика аутентификации для хэширования паролей и проверки пользователей."""

from typing import TYPE_CHECKING

from passlib.context import CryptContext

from app.exceptions import InvalidCredentialsError
from app.security import verify_password

if TYPE_CHECKING:
    from fastapi.security import HTTPBasicCredentials

    from app.repositories.user_repository import UserRepository
    from app.schemas.user import InternalUser


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


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
