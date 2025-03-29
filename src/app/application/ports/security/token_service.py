"""Интерфейс сервиса для создания и валидации JWT токенов."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


class TokenService(ABC):
    """Интерфейс для генерации и валидации JWT."""

    @abstractmethod
    def create_access_token(self, data: dict[str, 'Any']) -> str:
        """Создаёт access токен."""
        pass

    @abstractmethod
    def decode_access_token(self, token: str) -> dict[str, 'Any']:
        """Декодирует access токен."""
        pass
