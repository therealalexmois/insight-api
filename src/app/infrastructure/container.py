"""Контейнер зависимостей для управления синглтонами приложения."""

from typing import TYPE_CHECKING

from src.app.domain.constants import LOGGER_NAME
from src.app.infrastructure.adapters.logger.structlog_logger import StructlogLogger
from src.app.infrastructure.adapters.repositories.in_memory_user_repository import InMemoryUserRepository
from src.app.infrastructure.adapters.security.bcrypt_security_service import BcryptSecurityService

if TYPE_CHECKING:
    from src.app.application.ports.logger import Logger
    from src.app.application.ports.security import SecurityService
    from src.app.domain.repositories.user_repository import UserRepository


class AppContainer:
    """Контейнер синглтонов приложения.

    Служит для централизованного хранения и предоставления зависимостей.
    """

    _user_repository: 'UserRepository | None' = None
    _security_service: 'SecurityService' = BcryptSecurityService()

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
    def security_service(cls) -> 'SecurityService':
        """Возвращает синглтон менеджера безопасности.

        Returns:
            Экземпляр SecurityService.
        """
        return cls._security_service

    @classmethod
    def logger(cls) -> 'Logger':
        """Возвращает синглтон логгера приложения.

        Returns:
            Экземпляр Logger.
        """
        return StructlogLogger(name=LOGGER_NAME)
