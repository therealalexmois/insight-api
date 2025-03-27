"""Инициализирует репозиторий пользователей с тестовыми данными."""

from src.app.domain.models.user import InternalUser
from src.app.infrastructure.container import AppContainer


def init_fake_users() -> None:
    """Создаёт пользователей для разработки и тестов.

    Добавляет в репозиторий фиктивного пользователя с захардкоженными данными.
    """
    user_repository = AppContainer.user_repository()
    security_service = AppContainer.security_service()

    username = 'john_doe'

    if user_repository.get_by_username(username) is None:
        user = InternalUser(
            username=username,
            email='john@gmail.de',
            age=25,
            hashed_password=security_service.hash('qwerty123'),
        )
        user_repository.add(user)
