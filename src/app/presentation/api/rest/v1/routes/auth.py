"""Маршруты для аутентификации и выдачи JWT токенов."""

from http import HTTPStatus
from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.app.application.services.auth_service import authenticate_user
from src.app.infrastructure.container import AppContainer
from src.app.presentation.schemas.auth import Token

if TYPE_CHECKING:
    from src.app.domain.models.user import InternalUser

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)

OAuth2FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('token', status_code=HTTPStatus.OK, summary='Получить access токен')
def login_access_token(form_data: OAuth2FormDep) -> Token:
    """Аутентификация пользователя и выдача access токена.

    Args:
        form_data: Учетные данные (username и password) в форме OAuth2.

    Returns:
        JWT access токен, если аутентификация прошла успешно.
    """
    user: InternalUser = authenticate_user(
        form_data.username,
        form_data.password,
        AppContainer.password_hasher(),
        AppContainer.user_repository(),
    )

    access_token = AppContainer.token_service().create_access_token(
        {'sub': user.username, 'role': user.role.value},
    )

    return Token(access_token=access_token, token_type='bearer')
