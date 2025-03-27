"""Константы и перечисления, используемые в приложении."""

from enum import Enum


class AppEnv(str, Enum):
    """Перечисление окружений приложения."""

    LOCAL = 'local'
    DEV = 'dev'
    PROD = 'production'


class LogLevel(str, Enum):
    """Уровни журналирования в приложении."""

    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
