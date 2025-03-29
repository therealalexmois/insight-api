"""Presenter для преобразования моделей пользователя домена в модели ответа API."""

from typing import TYPE_CHECKING

from src.app.presentation.schemas.user import UserResponse

if TYPE_CHECKING:
    from src.app.domain.models.user import InternalUser


class UserPresenter:
    """Presenter для преобразования доменной модели пользователя в ответ API."""

    @staticmethod
    def to_response(user: 'InternalUser') -> 'UserResponse':
        """Преобразует доменную модель пользователя в схему ответа API.

        Args:
            user: Доменная модель пользователя.

        Returns:
            Модель ответа пользователя для API.
        """
        return UserResponse.model_validate(user, from_attributes=True)
