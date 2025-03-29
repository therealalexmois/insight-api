"""Инициализация маршрутов версии API v1."""

from fastapi import APIRouter

from src.app.presentation.api.constants import API_V1_PREFIX
from src.app.presentation.api.rest.v1.routes.admin import router as admin_router
from src.app.presentation.api.rest.v1.routes.health import router as health_router
from src.app.presentation.api.rest.v1.routes.predictions import router as predictions_router
from src.app.presentation.api.rest.v1.routes.users import router as users_router

api_v1_router = APIRouter(prefix=API_V1_PREFIX)

api_v1_router.include_router(admin_router)
api_v1_router.include_router(health_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(predictions_router)
