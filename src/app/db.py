"""Поддельная база данных пользователей in-memory, используемая для аутентификации и тестирования."""

from app.auth import get_password_hash
from app.config import DEFAULT_SECRET_KEY
from app.models import InternalUser

fake_users_db: dict[str, InternalUser] = {
    'john_doe': InternalUser(
        username='john_doe',
        hashed_password=get_password_hash(DEFAULT_SECRET_KEY),
        email='john@gmail.de',
        age=25,
    )
}
