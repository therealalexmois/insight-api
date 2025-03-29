"""Инициализирует репозиторий пользователей с тестовыми данными."""

from src.app.domain.models.user import InternalUser
from src.app.domain.value_objects.role import Role
from src.app.infrastructure.container import AppContainer


def init_fake_users() -> None:
    """Создаёт пользователей для разработки и тестов.

    Добавляет в репозиторий фиктивного пользователя с захардкоженными данными.
    """
    user_repository = AppContainer.user_repository()
    password_hasher = AppContainer.password_hasher()

    username = 'john_doe'

    if user_repository.get_by_username(username) is None:
        user = InternalUser(
            username=username,
            email='john@gmail.de',
            age=25,
            role=Role.USER,
            hashed_password=password_hasher.hash('qwerty123'),
        )
        user_repository.add(user)
