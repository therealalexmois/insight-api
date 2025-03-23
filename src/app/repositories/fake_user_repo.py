"""Заглушка репозитория пользователей."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import InternalUser

fake_users_db: dict[str, 'InternalUser'] = {}
