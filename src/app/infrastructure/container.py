"""Контейнер зависимостей для управления синглтонами приложения."""

from typing import TYPE_CHECKING

from src.app.domain.constants import LOGGER_NAME
from src.app.infrastructure.adapters.logger.structlog_logger import StructlogLogger
from src.app.infrastructure.adapters.repositories.in_memory_user_repository import InMemoryUserRepository
from src.app.infrastructure.adapters.security.bcrypt_password_hasher import BcryptPasswordHasher
from src.app.infrastructure.adapters.security.jwt_token_service import PyJWTTokenService
from src.app.infrastructure.config import get_settings

if TYPE_CHECKING:
    from src.app.application.ports.logger import Logger
    from src.app.application.ports.security.password_hasher import PasswordHasher
    from src.app.application.ports.security.token_service import TokenService
    from src.app.domain.repositories.user_repository import UserRepository


settings = get_settings()


class AppContainer:
    """Контейнер синглтонов приложения.

    Служит для централизованного хранения и предоставления зависимостей.
    """

    _user_repository: 'UserRepository | None' = None
    _password_hasher: 'PasswordHasher' = BcryptPasswordHasher()
    _token_service: 'TokenService' = PyJWTTokenService(
        secret_key=settings.app.secret_key.get_secret_value(),
        algorithm=settings.jwt.algorithm,
        expiration=settings.jwt.access_token_expiration,
    )

    @classmethod
    def user_repository(cls) -> 'UserRepository':
        """Возвращает синглтон репозитория пользователей.

        Returns:
            Экземпляр UserRepository.
        """
        if cls._user_repository is None:
            cls._user_repository = InMemoryUserRepository()
        return cls._user_repository

    @classmethod
    def password_hasher(cls) -> 'PasswordHasher':
        """Возвращает синглтон хешера паролей.

        Returns:
            Экземпляр PasswordHasher.
        """
        return cls._password_hasher

    @classmethod
    def token_service(cls) -> 'TokenService':
        """Возвращает синглтон службы токенов.

        Returns:
            Экземпляр TokenService.
        """
        return cls._token_service

    @classmethod
    def logger(cls) -> 'Logger':
        """Возвращает синглтон логгера приложения.

        Returns:
            Экземпляр Logger.
        """
        return StructlogLogger(name=LOGGER_NAME)
