import pytest

from src.app.domain.repositories.user_repository import UserRepository
from src.app.infrastructure.container import AppContainer
from src.app.presentation.dependencies import get_user_repository


@pytest.mark.unit
def test_get_user_repository__returns_singleton_instance() -> None:
    """Должен возвращать тот же экземпляр user_repository, что и в контейнере."""
    user_repository = get_user_repository()

    assert isinstance(user_repository, UserRepository)
    assert user_repository is AppContainer.user_repository()
