"""Точка входа в приложение FastAPI. Настраивает и запускает сервер."""

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.config import get_settings
from app.exceptions import base_app_error_handler, BaseAppError, validation_error_handler
from app.logging import configure_logging
from app.predict import router as predict_router
from app.users import router as users_router

settings = get_settings()


def create_app() -> FastAPI:
    """Создает и настраивает экземпляр FastAPI-приложения.

    Returns:
        Объект FastAPI с подключёнными маршрутами.
    """
    configure_logging()

    app = FastAPI(
        title=settings.app.name,
        version=settings.app.version,
        description=settings.app.description,
        debug=settings.app.debug,
    )
    app.include_router(users_router)
    app.include_router(predict_router)
    app.add_exception_handler(BaseAppError, base_app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    return app


def start_app() -> None:
    """Запускает приложение с помощью uvicorn.

    Используется в локальной разработке через Makefile.
    """
    uvicorn.run(
        'src.app.main:create_app()',
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
    )


if __name__ == '__main__':
    start_app()
