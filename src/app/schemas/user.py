"""Pydantic-схемы для работы с прогнозами."""

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Схема регистрации нового пользователя."""

    username: str
    email: EmailStr
    age: int
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


class User(BaseModel):
    """Публичная модель пользователя, возвращаемая API."""

    username: str
    email: str
    age: int

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


class InternalUser(User):
    """Внутренняя модель пользователя, используемая при аутентификации."""

    hashed_password: str
