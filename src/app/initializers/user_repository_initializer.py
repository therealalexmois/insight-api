"""Инициализирует репозиторий пользователей с тестовыми данными."""

from app.auth import get_password_hash
from app.config import get_settings
from app.models import InternalUser
from app.repositories.in_memory_user_repository import InMemoryUserRepository

user_repository = InMemoryUserRepository()


def init_fake_users() -> None:
    """Создает пользователей для разработки и тестов."""
    settings = get_settings()

    user_repository.add(
        InternalUser(
            username='john_doe',
            hashed_password=get_password_hash(settings.app.secret_key.get_secret_value()),
            email='john@gmail.de',
            age=25,
        )
    )
