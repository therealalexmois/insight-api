"""Схемы для работы с JWT-аутентификацией."""

from pydantic import BaseModel, Field


class Token(BaseModel):
    """Схема возвращаемого токена доступа."""

    access_token: str = Field(..., description='JWT токен доступа')
    token_type: str = Field(default='bearer', description='Тип токена (по умолчанию bearer)')


class TokenData(BaseModel):
    """Схема данных, извлекаемых из токена."""

    username: str | None = Field(default=None, description='Имя пользователя, полученное из JWT')
