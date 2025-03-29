"""Маршрут администратора."""

from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.app.presentation.webserver.dependencies import AdminUserDep  # noqa: TC001

router = APIRouter()


@router.get('admin', status_code=HTTPStatus.OK, summary='Admin Check')
def admin(current_user: AdminUserDep) -> JSONResponse:
    """Проверяет, что текущий пользователь имеет роль администратора.

    Args:
        current_user: Аутентифицированный пользователь с ролью ADMIN.

    Returns:
        Ответ с приветствием, если доступ разрешён.
    """
    return JSONResponse(content={'message': f'Hello admin {current_user.username}'})
