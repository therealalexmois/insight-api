"""Схемы Pydantic для работы с пользователями через API."""

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
                    'email': 'user@example.com',
                    'age': 30,
                    'password': 'supersecret123',
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """Схема ответа API с данными пользователя."""

    username: str
    email: str
    age: int

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'username': 'john_doe',
                    'email': 'john@example.com',
                    'age': 25,
                }
            ]
        }
    }
