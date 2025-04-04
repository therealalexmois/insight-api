"""Точка входа в приложение. Настраивает и запускает сервер."""

import os
import pathlib

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.app.domain.exceptions import BaseAppError
from src.app.infrastructure.adapters.logger.logging import configure_logging
from src.app.infrastructure.adapters.logger.structlog_logger import StructlogLogger
from src.app.infrastructure.config import get_settings
from src.app.infrastructure.initializers.user_repository_initializer import init_fake_users
from src.app.presentation.api.rest.v1.router import api_v1_router
from src.app.presentation.webserver.exceptions import base_app_error_handler, validation_error_handler
from src.app.presentation.webserver.middlewares.request_id import request_id_middleware
from src.app.presentation.webserver.middlewares.request_logging import request_logging_middleware

settings = get_settings()


def create_app() -> FastAPI:
    """Создает и настраивает экземпляр FastAPI-приложения.

    Returns:
        Объект FastAPI с подключёнными маршрутами.
    """
    configure_logging(
        app_name=settings.app.name,
        app_version=settings.app.version,
        env=settings.app.env,
        instance=settings.app.host,
        log_level=settings.logging.level,
    )

    init_fake_users()

    app = FastAPI(
        docs_url=None,
        redoc_url='/',
        title=settings.app.name,
        version=settings.app.version,
        description=settings.app.description,
        debug=settings.app.debug,
    )

    app.include_router(api_v1_router)

    app.add_exception_handler(BaseAppError, base_app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)

    app.middleware('http')(request_logging_middleware)
    app.middleware('http')(request_id_middleware)

    return app


def start_app() -> None:
    """Запускает приложение с помощью uvicorn."""
    logger = StructlogLogger('uvicorn')

    current_dir = str(pathlib.Path.cwd())

    logger.info('Will watch for changes in these directories', extra={'directories': [current_dir]})
    logger.info(f'Uvicorn running on http://{settings.app.host}:{settings.app.port} (Press CTRL+C to quit)')
    logger.info('Started reloader process', extra={'pid': os.getpid(), 'reloader': 'StatReload'})

    uvicorn.run(
        # TODO: Вынести в конфиг
        'src.app.main:create_app',
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
        # TODO: Вынести в конфиг
        access_log=False,
        log_config=None,
        log_level=settings.logging.level.value,
        # TODO: Вынести в конфиг
        factory=True,
    )


if __name__ == '__main__':
    start_app()
