"""Абстрактный репозиторий для управления пользователями."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import InternalUser


class UserRepository(ABC):
    """Абстрактный репозиторий для управления пользователями."""

    @abstractmethod
    def add(self, user: 'InternalUser') -> None:
        """Добавляет пользователя в репозиторий.

        Args:
            user: Пользователь для добавления.
        """
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> 'InternalUser | None':
        """Возвращает пользователя по имени (без учета регистра).

        Args:
            username: Имя пользователя.

        Returns:
            Найденный пользователь или None.
        """
        pass

    @abstractmethod
    def list(self) -> list['InternalUser']:
        """Возвращает список всех пользователей.

        Returns:
            Список пользователей.
        """
        pass
