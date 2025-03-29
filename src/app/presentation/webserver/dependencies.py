"""Зависимости FastAPI для повторного использования логики."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from jwt import PyJWTError

from src.app.application.ports.security.password_hasher import PasswordHasher
from src.app.application.ports.security.token_service import TokenService
from src.app.application.services.auth_service import resolve_current_user, verify_password
from src.app.domain.models.user import InternalUser, User
from src.app.domain.repositories.user_repository import UserRepository
from src.app.infrastructure.config import get_settings, Settings
from src.app.infrastructure.container import AppContainer
from src.app.presentation.api.constants import OAUTH2_TOKEN_URL
from src.app.presentation.webserver.exceptions import build_unauthorized_exception

http_basic_security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=OAUTH2_TOKEN_URL)


def get_app_settings() -> 'Settings':
    """Возвращает экземпляр настроек приложения."""
    return get_settings()


def get_user_repository() -> 'UserRepository':
    """Возвращает экземпляр репозитория пользователей."""
    return AppContainer.user_repository()


def get_password_hasher() -> 'PasswordHasher':
    """Возвращает экземпляр хешера паролей."""
    return AppContainer.password_hasher()


def get_token_service() -> 'TokenService':
    """Возвращает экземпляр службы токенов."""
    return AppContainer.token_service()


AppSettingsDep = Annotated[Settings, Depends(get_app_settings)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
CredentialsDep = Annotated[HTTPBasicCredentials, Depends(http_basic_security)]
UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
HasherDep = Annotated[PasswordHasher, Depends(get_password_hasher)]
TokenServiceDep = Annotated[TokenService, Depends(get_token_service)]


def get_current_user_oauth2(
    token: TokenDep,
    token_service: TokenServiceDep,
    user_repository: UserRepoDep,
) -> User:
    """Получает текущего пользователя из JWT-токена.

    Args:
        token: JWT-токен из запроса.
        token_service: Сервис для декодирования токена.
        user_repository: Репозиторий пользователей.

    Returns:
        Объект пользователя.

    Raises:
        HTTPException: Если токен недействителен или пользователь не найден.
    """
    try:
        payload = token_service.decode_access_token(token)
        username = payload.get('sub')
        if not username:
            raise build_unauthorized_exception(detail='Invalid authentication token')
    except PyJWTError as error:
        raise build_unauthorized_exception(detail='Invalid token or expired') from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal authentication error'
        ) from error

    return resolve_current_user(username, user_repository)


def get_current_user_http_basic(
    credentials: CredentialsDep,
    password_hasher: HasherDep,
    user_repository: UserRepoDep,
) -> 'InternalUser':
    """Зависимость для получения текущего аутентифицированного пользователя.

    Args:
        credentials: Учетные данные HTTP Basic.
        password_hasher: Сервиса хеширования паролей.
        user_repository: Репозиторий пользователей.

    Returns:
        Внутренняя модель пользователя, если аутентификация прошла успешно.
    """
    user = resolve_current_user(credentials.username, user_repository)
    verify_password(credentials.password, user.hashed_password, password_hasher)
    return user


CurrentUserDep = Annotated[InternalUser, Depends(get_current_user_http_basic)]
