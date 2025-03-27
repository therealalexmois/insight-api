"""Инфраструктурная реализация PasswordHasher с использованием bcrypt и SHA-512."""

import hashlib
from typing import cast

from passlib.context import CryptContext

from src.app.application.ports.security import SecurityService
from src.app.presentation.config import get_settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class BcryptSecurityService(SecurityService):
    """Хешер паролей с SHA-512 + bcrypt."""

    def __init__(self) -> None:
        """Инициализирует хешер, извлекая секретный ключ из конфигурации приложения.

        Секретный ключ используется при прехешировании пароля перед применением bcrypt.
        """
        self._secret = get_settings().app.secret_key.get_secret_value()

    def _prehash(self, password: str) -> str:
        """Прехеширует пароль с использованием SHA-512 и секретного ключа.

        Эта функция объединяет пароль пользователя с секретным ключом приложения и
        хеширует полученную строку с использованием SHA-512.

        Args:
            password: Исходный пароль пользователя.

        Returns:
            SHA-512 хеш от пароля с солью.
        """
        salted = f'{password}{self._secret}'
        return hashlib.sha512(salted.encode()).hexdigest()

    def hash(self, password: str) -> str:
        """Возвращает хеш от переданного пароля.

        Применяет SHA-512 прехеширование с секретным ключом, а затем хеширует результат с помощью bcrypt.

        Args:
            password: Исходный пароль пользователя.

        Returns:
            Хешированная строка, пригодная для хранения в БД.
        """
        prehashed = self._prehash(password)
        return cast('str', pwd_context.hash(prehashed))

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Проверяет соответствие пароля его хешу.

        Применяет SHA-512 прехеширование к переданному паролю и сверяет его с сохранённым bcrypt-хешем.

        Args:
            plain_password: Исходный (введённый) пароль пользователя.
            hashed_password: Хеш, сохранённый в базе данных.

        Returns:
            True, если хеш соответствует паролю. Иначе — False.
        """
        prehashed = self._prehash(plain_password)
        return cast('bool', pwd_context.verify(prehashed, hashed_password))
