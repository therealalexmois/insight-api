"""Реализация in-memory репозитория пользователей."""

from typing import TYPE_CHECKING

from src.app.domain.repositories.user_repository import UserRepository

if TYPE_CHECKING:
    from src.app.domain.models.user import InternalUser


class InMemoryUserRepository(UserRepository):
    """Ин-мемори реализация репозитория пользователей."""

    def __init__(self) -> None:
        """Инициализирует пустой словарь пользователей."""
        self._users: dict[str, InternalUser] = {}

    def add(self, user: 'InternalUser') -> None:
        """Добавляет пользователя в репозиторий.

        Args:
            user: Пользователь для добавления.
        """
        self._users[user.username.lower()] = user

    def get_by_username(self, username: str) -> 'InternalUser | None':
        """Возвращает пользователя по имени без учета регистра.

        Args:
            username: Имя пользователя.

        Returns:
            Пользователь или None, если не найден.
        """
        return self._users.get(username.lower())

    def list(self) -> list['InternalUser']:
        """Возвращает всех пользователей из репозитория.

        Returns:
            Список пользователей.
        """
        return list(self._users.values())
