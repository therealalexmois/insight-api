import pytest

from src.app.container import app_container
from src.app.dependencies import get_user_repository
from src.app.repositories.user_repository import UserRepository


@pytest.mark.unit
def test_get_user_repository__returns_singleton_instance() -> None:
    """Должен возвращать тот же экземпляр user_repository, что и в контейнере."""
    user_repository = get_user_repository()

    assert isinstance(user_repository, UserRepository)
    assert user_repository is app_container.user_repository()
