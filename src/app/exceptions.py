"""Пользовательские ошибки и обработчики исключений."""

from typing import TYPE_CHECKING

import structlog
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.error_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

if TYPE_CHECKING:
    from fastapi import Request


log = structlog.get_logger()


class BaseAppError(Exception):
    """Базовая ошибка приложения."""

    def __init__(self, message: str, status_code: int = HTTP_400_BAD_REQUEST) -> None:
        """Инициализирует ошибку приложения с сообщением и HTTP-статусом.

        Args:
            message: Текстовое описание ошибки.
            status_code: HTTP-код, возвращаемый клиенту.
        """
        self.message = message
        self.status_code = status_code


class UserAlreadyExistsError(BaseAppError):
    """Ошибка: пользователь с таким именем уже существует."""

    def __init__(self) -> None:
        """Инициализирует ошибку конфликта при создании пользователя.

        HTTP 409 Conflict.
        """
        super().__init__('User already exists', status_code=HTTP_409_CONFLICT)


class UserNotFoundError(BaseAppError):
    """Ошибка: пользователь не найден."""

    def __init__(self) -> None:
        """Ошибка при попытке получить несуществующего пользователя.

        HTTP 404 Not Found.
        """
        super().__init__('User not found', status_code=HTTP_404_NOT_FOUND)


class InvalidCredentialsError(BaseAppError):
    """Ошибка: неверное имя пользователя или пароль."""

    def __init__(self) -> None:
        """Ошибка аутентификации.

        HTTP 401 Unauthorized.
        """
        super().__init__('Incorrect username or password', status_code=HTTP_401_UNAUTHORIZED)


async def base_app_error_handler(_: 'Request', exc: Exception) -> JSONResponse:
    """Обработчик ошибок для BaseAppError.

    Args:
        _: Неиспользуемый объект запроса.
        exc: Исключение, ожидаемое как BaseAppException.

    Returns:
        JSON-ответ с сообщением об ошибке и статусом.
    """
    if isinstance(exc, BaseAppError):
        log.warning('application_error', message=exc.message, status_code=exc.status_code)
        return JSONResponse(
            status_code=exc.status_code,
            content={'detail': exc.message},
        )

    log.error('unexpected_exception', exc_info=exc)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={'detail': 'Internal Server Error'},
    )


async def validation_error_handler(_: 'Request', exc: 'Exception') -> JSONResponse:
    """Обработчик ошибок валидации запроса.

    Args:
        exc: Исключение, ожидаемое как RequestValidationError.

    Returns:
        JSON-ответ с ошибками валидации.
    """
    if isinstance(exc, RequestValidationError):
        log.warning('validation_error', errors=exc.errors())
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={'detail': exc.errors()},
        )

    log.error('unexpected_validation_handler_path', exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={'detail': 'Internal Server Error'},
    )
