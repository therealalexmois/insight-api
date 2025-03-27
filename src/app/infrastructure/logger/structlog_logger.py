"""Реализация интерфейса логгера с использованием библиотеки structlog."""

import structlog

from src.app.application.ports.logger import Logger


class StructlogLogger(Logger):
    """Логгер, реализующий интерфейс Logger через structlog."""

    def __init__(self) -> None:
        """Инициализирует экземпляр structlog логгера."""
        self._logger = structlog.get_logger()

    def info(self, event: str, **kwargs: object) -> None:
        """Логгирует информационное сообщение.

        Args:
            event: Название события.
            **kwargs: Дополнительные параметры события.
        """
        self._logger.info(event, **kwargs)

    def warning(self, event: str, **kwargs: object) -> None:
        """Логгирует предупреждающее сообщение.

        Args:
            event: Название события.
            **kwargs: Дополнительные параметры события.
        """
        self._logger.warning(event, **kwargs)

    def error(self, event: str, **kwargs: object) -> None:
        """Логгирует сообщение об ошибке.

        Args:
            event: Название события.
            **kwargs: Дополнительные параметры события.
        """
        self._logger.error(event, **kwargs)
