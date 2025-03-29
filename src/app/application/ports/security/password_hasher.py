"""Контракт для сервиса хеширования паролей."""

from abc import ABC, abstractmethod


class PasswordHasher(ABC):
    """Интерфейс сервиса хеширования паролей."""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Возвращает хеш от пароля."""
        pass

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Проверяет соответствие пароля и его хеша."""
        pass
