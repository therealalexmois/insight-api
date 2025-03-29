"""Адаптер сервиса для работы с JWT токенами."""

from datetime import datetime, timedelta, UTC
from typing import cast, TYPE_CHECKING

import jwt

from src.app.application.ports.security.token_service import TokenService
from src.app.domain.exceptions import InvalidTokenError
from src.app.infrastructure.config import get_settings

if TYPE_CHECKING:
    from typing import Any


settings = get_settings()


class PyJWTTokenService(TokenService):
    """Реализация TokenService с использованием библиотеки PyJWT."""

    def __init__(self, secret_key: str, algorithm: str, expiration: timedelta) -> None:
        """Инициализирует JWT сервис.

        Args:
            secret_key: Секретный ключ для подписи JWT-токенов.
            algorithm: Алгоритм кодирования и декодирования JWT.
            expiration: Срок действия access токена.
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expiration = expiration

    def create_access_token(self, data: dict[str, 'Any']) -> str:
        """Создаёт access токен с подписью и сроком действия.

        Args:
            data: Пользовательские данные, включаемые в токен. Ожидаются поля 'sub' и 'role'.

        Returns:
            Закодированный JWT access токен.
        """
        payload = data.copy()
        payload['exp'] = datetime.now(UTC) + self.expiration

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_access_token(self, token: str) -> dict[str, 'Any']:
        """Декодирует и валидирует access токен.

        Args:
            token: JWT access токен, полученный от клиента.

        Returns:
            Раскодированные данные токена в виде словаря.

        Raises:
            InvalidTokenError: Если токен недействителен или истёк.
        """
        try:
            return cast('dict[str, Any]', jwt.decode(token, self.secret_key, algorithms=[self.algorithm]))
        except jwt.PyJWTError as error:
            raise InvalidTokenError() from error
