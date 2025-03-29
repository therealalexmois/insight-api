"""Адаптер сервиса для работы с JWT токенами."""

from datetime import datetime, timedelta, UTC
from typing import cast, TYPE_CHECKING

import jwt

if TYPE_CHECKING:
    from typing import Any


from src.app.application.ports.security.token_service import TokenService
from src.app.infrastructure.config import get_settings

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
        """Создаёт access токен с подписью и сроком действия."""
        payload = data.copy()
        payload['exp'] = datetime.now(UTC) + self.expiration
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_access_token(self, token: str) -> dict[str, 'Any']:
        """Декодирует и валидирует access токен."""
        return cast('dict[str, Any]', jwt.decode(token, self.secret_key, algorithms=[self.algorithm]))
