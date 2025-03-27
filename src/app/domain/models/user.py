"""Доменная модель пользователя."""

from dataclasses import dataclass
from typing import Final  # noqa: TC003

DEFAULT_ADULT_AGE: Final[int] = 18


@dataclass(frozen=True)
class User:
    """Пользователь, используемый в бизнес-логике."""

    username: str
    email: str
    age: int

    def is_adult(self) -> bool:
        """Проверяет, является ли пользователь совершеннолетним.

        Returns:
            True, если пользователю 18 лет и более.
        """
        return self.age >= DEFAULT_ADULT_AGE


# TODO: Убрать эту модель
@dataclass(frozen=True)
class InternalUser(User):
    """Внутренняя модель пользователя, содержащая хеш пароля.

    Используется при аутентификации и работе с репозиторием.
    """

    hashed_password: str
