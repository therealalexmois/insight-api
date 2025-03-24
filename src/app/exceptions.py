"""Пользовательские ошибки и обработчики исключений."""

from http import HTTPStatus
from typing import TYPE_CHECKING

import structlog
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from collections.abc import Sequence

    from fastapi import Request


log = structlog.get_logger()


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

    def __init__(self) -> None:
        """Инициализирует ошибку конфликта при создании пользователя.

        HTTP 409 Conflict.
        """
        super().__init__('User already exists', status_code=HTTPStatus.CONFLICT)


class UserNotFoundError(BaseAppError):
    """Ошибка: пользователь не найден."""

    def __init__(self) -> None:
        """Ошибка при попытке получить несуществующего пользователя.

        HTTP 404 Not Found.
        """
        super().__init__('User not found', status_code=HTTPStatus.NOT_FOUND)


class InvalidCredentialsError(BaseAppError):
    """Ошибка: неверное имя пользователя или пароль."""

    def __init__(self) -> None:
        """Ошибка аутентификации.

        HTTP 401 Unauthorized.
        """
        super().__init__('Incorrect username or password', status_code=HTTPStatus.UNAUTHORIZED)


async def base_app_error_handler(_: 'Request', exc: Exception) -> JSONResponse:
    """Обработчик ошибок приложения.

    Args:
        _: Объект запроса (не используется).
        exc: Исключение, которое должно быть экземпляром BaseAppError.

    Returns:
        JSON-ответ с сообщением об ошибке и HTTP-статусом.
    """
    if isinstance(exc, BaseAppError):
        log.warning('application_error', message=exc.message, status_code=exc.status_code)
        return _internal_error_response(status_code=exc.status_code, content=exc.message)

    log.error('unexpected_exception', exc_info=exc)
    return _internal_error_response(
        status_code=int(HTTPStatus.INTERNAL_SERVER_ERROR),
        content=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
    )


async def validation_error_handler(_: 'Request', exc: 'Exception') -> JSONResponse:
    """Обработчик ошибок приложения.

    Args:
        _: Объект запроса (не используется).
        exc: Исключение, которое должно быть экземпляром BaseAppError.

    Returns:
        JSON-ответ с сообщением об ошибке и HTTP-статусом.
    """
    if isinstance(exc, RequestValidationError):
        log.warning('validation_error', errors=exc.errors())
        return _internal_error_response(status_code=int(HTTPStatus.BAD_REQUEST), content=exc.errors())

    log.error('unexpected_validation_handler_path', exc_info=exc)
    return _internal_error_response(
        status_code=int(HTTPStatus.INTERNAL_SERVER_ERROR),
        content=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
    )


def _internal_error_response(status_code: int, content: 'str | Sequence[dict[str, object]]') -> JSONResponse:
    """Формирует JSON-ответ с заданным HTTP-статусом и телом ошибки.

    Args:
        status_code: HTTP-статус ответа.
        content: Содержимое поля `detail` в теле ответа.

    Returns:
        Объект JSONResponse с заданными параметрами.
    """
    return JSONResponse(
        status_code=status_code,
        content={'detail': content},
    )
