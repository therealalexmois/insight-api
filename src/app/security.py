"""Функции безопасности для работы с паролями.

Содержит утилиты для хеширования паролей и проверки их корректности с использованием bcrypt.
"""

from typing import cast

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля на его хэшированный аналог.

    Args:
        plain_password: Необработанный пароль, предоставленный пользователем.
        hashed_password: Хешированный пароль, хранящийся в базе данных.

    Returns:
        True, если пароль действителен, False - в противном случае.
    """
    return cast('bool', pwd_context.verify(plain_password, hashed_password))


def get_password_hash(password: str) -> str:
    """Хеширование пароля с помощью bcrypt.

    Args:
        password: Необработанный пароль, предоставленный пользователем.

    Returns:
        Хешированная строка пароля.
    """
    return cast('str', pwd_context.hash(password))
