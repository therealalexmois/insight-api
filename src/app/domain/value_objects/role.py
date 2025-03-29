"""Роль пользователя в доменной модели."""

from enum import Enum


class Role(str, Enum):
    """Роль пользователя."""

    USER = 'user'
    ADMIN = 'admin'
