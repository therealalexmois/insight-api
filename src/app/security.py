"""Функции безопасности для работы с паролями.

Содержит утилиты для хеширования паролей и проверки их корректности с использованием bcrypt.
"""

import hashlib
from typing import cast

from passlib.context import CryptContext

from app.config import get_settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


settings = get_settings()


def _prehash(password: str) -> str:
    """Прехеширование пароля с использованием SHA-512 и секретного ключа."""
    salted = f'{password}{settings.app.secret_key.get_secret_value()}'
    return hashlib.sha512(salted.encode()).hexdigest()


def get_password_hash(password: str) -> str:
    """Хеширование пароля с помощью bcrypt.

    Args:
        password: Необработанный пароль, предоставленный пользователем.

    Returns:
        Хешированная строка пароля.
    """
    prehashed = _prehash(password)
    return cast('str', pwd_context.hash(prehashed))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля на его хэшированный аналог.

    Args:
        plain_password: Необработанный пароль, предоставленный пользователем.
        hashed_password: Хешированный пароль, хранящийся в базе данных.

    Returns:
        True, если пароль действителен, False - в противном случае.
    """
    prehashed = _prehash(plain_password)
    return cast('bool', pwd_context.verify(prehashed, hashed_password))
