"""Точка входа в приложение. Настраивает и запускает сервер."""

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.config import get_settings
from app.exceptions import base_app_error_handler, BaseAppError, validation_error_handler
from app.initializers.user_repository_initializer import init_fake_users
from app.logging.logging import configure_logging
from app.middleware.logging_middleware import logging_middleware
from app.predict import router as predict_router
from app.users import router as users_router

settings = get_settings()


def create_app() -> FastAPI:
    """Создает и настраивает экземпляр FastAPI-приложения.

    Returns:
        Объект FastAPI с подключёнными маршрутами.
    """
    configure_logging()

    init_fake_users()

    app = FastAPI(
        docs_url=None,
        redoc_url='/',
        title=settings.app.name,
        version=settings.app.version,
        description=settings.app.description,
        debug=settings.app.debug,
    )
    app.include_router(users_router)
    app.include_router(predict_router)
    app.add_exception_handler(BaseAppError, base_app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.middleware('http')(logging_middleware)
    return app


def start_app() -> None:
    """Запускает приложение с помощью uvicorn."""
    uvicorn.run(
        'src.app.main:create_app',
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
        factory=True,
    )


if __name__ == '__main__':
    start_app()
