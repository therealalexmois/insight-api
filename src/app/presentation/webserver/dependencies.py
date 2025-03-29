"""Зависимости FastAPI для повторного использования логики."""

from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer

from src.app.application.ports.security.password_hasher import PasswordHasher
from src.app.application.ports.security.token_service import TokenService
from src.app.application.services.auth_service import authenticate_user, resolve_current_user
from src.app.domain.exceptions import InvalidTokenError
from src.app.domain.models.user import InternalUser, User
from src.app.domain.repositories.user_repository import UserRepository
from src.app.domain.value_objects.role import Role
from src.app.infrastructure.config import get_settings, Settings
from src.app.infrastructure.container import AppContainer
from src.app.presentation.api.constants import OAUTH2_TOKEN_URL
from src.app.presentation.schemas.auth import TokenData
from src.app.presentation.webserver.exceptions import build_unauthorized_exception

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable


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
    username, password = credentials.username, credentials.password
    user = authenticate_user(
        username=username, password=password, user_repository=user_repository, password_hasher=password_hasher
    )
    return user


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
        token_data = TokenData(**payload)
        if not token_data.username or not token_data.role:
            raise build_unauthorized_exception(detail='Invalid authentication token')
    except InvalidTokenError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal authentication error'
        ) from error

    user: InternalUser = resolve_current_user(token_data.username, user_repository)
    return user


CurrentUserHTTPBasicDep = Annotated[InternalUser, Depends(get_current_user_http_basic)]
CurrentUserOauth2Dep = Annotated[InternalUser, Depends(get_current_user_oauth2)]


def require_roles(allowed_roles: 'Iterable[Role]') -> 'Callable[[Annotated[InternalUser, Depends]], InternalUser]':
    """Фабрика зависимости для проверки принадлежности пользователя к одной из допустимых ролей.

    Args:
        allowed_roles: Список разрешённых ролей.

    Returns:
        Зависимость FastAPI, проверяющая роль пользователя.
    """

    def dependency(user: InternalUser) -> InternalUser:
        """Проверяет, входит ли роль пользователя в список разрешённых.

        Args:
            user: Аутентифицированный пользователь.

        Returns:
            Объект InternalUser, если роль разрешена.

        Raises:
            HTTPException: Если у пользователя нет нужных прав.
        """
        if user.role not in allowed_roles:
            raise build_unauthorized_exception('Недостаточно прав доступа')
        return user

    return dependency


AdminUserDep = Annotated[InternalUser, Depends(require_roles([Role.ADMIN]))]
