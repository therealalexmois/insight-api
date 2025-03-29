"""Инициализация маршрутов версии API v1."""

from fastapi import APIRouter

from src.app.presentation.api.v1.routes.health import router as health_router
from src.app.presentation.api.v1.routes.users import router as users_router
from src.app.presentation.api.v1.routes.predictions import router as predictions_router

api_v1_router = APIRouter(prefix='/api/v1')

api_v1_router.include_router(health_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(predictions_router)
