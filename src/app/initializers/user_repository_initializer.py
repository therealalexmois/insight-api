"""Инициализирует репозиторий пользователей с тестовыми данными."""

from app.container import app_container
from app.schemas.user import InternalUser
from app.security import get_password_hash


def init_fake_users() -> None:
    """Создает пользователей для разработки и тестов."""
    user_repository = app_container.user_repository()

    user = InternalUser(
        username='john_doe',
        hashed_password=get_password_hash('test1234'),
        email='john@gmail.de',
        age=25,
    )

    user_repository.add(user)
