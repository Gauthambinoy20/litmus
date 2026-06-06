import logging

import structlog

from app.config import get_settings


def _renderer() -> structlog.types.Processor:
    if get_settings().environment == "development":
        return structlog.dev.ConsoleRenderer()
    return structlog.processors.JSONRenderer()


def setup_logging() -> None:
    settings = get_settings()
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            _renderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = "litmus") -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
