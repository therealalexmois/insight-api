"""Интерфейс логгера для использования в приложении."""

from abc import ABC, abstractmethod


class Logger(ABC):
    """Интерфейс логгера, абстрагирующий реализацию логирования."""

    @abstractmethod
    def info(self, event: str, **kwargs: object) -> None:
        """Логирует информационное сообщение."""
        pass

    @abstractmethod
    def warning(self, event: str, **kwargs: object) -> None:
        """Логирует предупреждение."""
        pass

    @abstractmethod
    def error(self, event: str, **kwargs: object) -> None:
        """Логирует ошибку."""
        pass
