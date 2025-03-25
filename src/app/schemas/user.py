"""Pydantic-схемы для работы с пользователями."""

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Базовая схема пользователя."""

    username: str
    email: EmailStr
    age: int


class UserCreate(UserBase):
    """Схема регистрации нового пользователя с открытым паролем."""

    password: str = Field(min_length=8, max_length=64)

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'username': 'new_user',
                    'email': 'new_user@example.com',
                    'age': 30,
                    'password': 'securepassword123',
                }
            ]
        }
    }


class User(UserBase):
    """Публичная модель пользователя, возвращаемая API."""

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'username': 'john_doe',
                    'email': 'john@gmail.de',
                    'age': 25,
                }
            ]
        }
    }


class InternalUser(UserBase):
    """Внутренняя модель пользователя, используемая при аутентификации."""

    hashed_password: str
