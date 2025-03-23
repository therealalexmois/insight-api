"""Поддельная база данных пользователей in-memory, используемая для аутентификации и тестирования."""

from app.auth import get_password_hash
from app.config import get_settings
from app.models import InternalUser

settings = get_settings()

fake_users_db: dict[str, InternalUser] = {
    'john_doe': InternalUser(
        username='john_doe',
        hashed_password=get_password_hash(settings.app.secret_key),
        email='john@gmail.de',
        age=25,
    )
}
