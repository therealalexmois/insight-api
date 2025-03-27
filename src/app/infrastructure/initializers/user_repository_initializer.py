"""Инициализирует репозиторий пользователей с тестовыми данными."""

from src.app.domain.models.user import InternalUser
from src.app.infrastructure.container import AppContainer


def init_fake_users() -> None:
    """Создаёт пользователей для разработки и тестов.

    Добавляет в репозиторий фиктивного пользователя с захардкоженными данными.
    """
    user_repository = AppContainer.user_repository()
    password_hasher = AppContainer.security_service()

    user = InternalUser(
        username='john_doe',
        email='john@gmail.de',
        age=25,
        hashed_password=password_hasher.hash('test1234'),
    )

    user_repository.add(user)
