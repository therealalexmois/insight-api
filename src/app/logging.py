"""Настройка логирования через structlog."""

import logging.config
import os

import structlog

ALLOWED_LOG_LEVELS = {'debug', 'info', 'error'}


def configure_logging() -> None:
    """Настраивает структуру логирования с использованием structlog."""
    log_level = os.getenv('LOG_LEVEL', 'info').lower()

    if log_level not in ALLOWED_LOG_LEVELS:
        log_level = 'info'

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'plain': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.dev.ConsoleRenderer(),
                'foreign_pre_chain': [
                    structlog.processors.TimeStamper(fmt='iso'),
                    structlog.stdlib.add_log_level,
                ],
            },
        },
        'handlers': {
            'default': {
                'level': log_level.upper(),
                'class': 'logging.StreamHandler',
                'formatter': 'plain',
            },
        },
        'root': {
            'level': log_level.upper(),
            'handlers': ['default'],
        },
    }

    logging.config.dictConfig(logging_config)

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
