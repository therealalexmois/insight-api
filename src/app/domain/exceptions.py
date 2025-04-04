"""Доменные ошибки, связанные с бизнес-логикой."""

from http import HTTPStatus


class BaseAppError(Exception):
    """Базовая ошибка приложения."""

    def __init__(self, message: str, status_code: HTTPStatus = HTTPStatus.BAD_REQUEST) -> None:
        """Инициализирует ошибку приложения с сообщением и HTTP-статусом.

        Args:
            message: Текстовое описание ошибки.
            status_code: HTTP-код, возвращаемый клиенту.
        """
        self.message = message
        self.status_code = int(status_code)


class UserAlreadyExistsError(BaseAppError):
    """Ошибка: пользователь с таким именем уже существует."""

    def __init__(self, username: str) -> None:
        """Ошибка конфликта при создании пользователя (HTTP 409).

        Args:
            username: Имя пользователя, вызвавшего ошибку.
        """
        super().__init__(f'User "{username}" already exists', status_code=HTTPStatus.CONFLICT)


class UserNotFoundError(BaseAppError):
    """Ошибка: пользователь не найден."""

    def __init__(self) -> None:
        """Ошибка при попытке получить несуществующего пользователя (HTTP 404)."""
        super().__init__('User not found', status_code=HTTPStatus.NOT_FOUND)


class InvalidCredentialsError(BaseAppError):
    """Ошибка: неверное имя пользователя или пароль."""

    def __init__(self) -> None:
        """Ошибка аутентификации (HTTP 401)."""
        super().__init__('Incorrect username or password', status_code=HTTPStatus.UNAUTHORIZED)


class InvalidTokenError(BaseAppError):
    """Ошибка: токен недействителен, подпись некорректна или срок действия истёк."""

    def __init__(self) -> None:
        """Ошибка аутентификации (HTTP 401)."""
        super().__init__('Invalid or expired token', status_code=HTTPStatus.UNAUTHORIZED)
