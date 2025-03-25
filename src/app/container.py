"""Контейнер зависимостей для управления синглтонами приложения."""

from src.app.repositories.in_memory_user_repository import InMemoryUserRepository


class AppContainer:
    """Контейнер синглтонов приложения."""

    _user_repository: InMemoryUserRepository | None = None

    @classmethod
    def user_repository(cls) -> InMemoryUserRepository:
        """Возвращает синглтон экземпляра InMemoryUserRepository."""
        if cls._user_repository is None:
            cls._user_repository = InMemoryUserRepository()
        return cls._user_repository
