import logging
import sys
import os

from logging.handlers import RotatingFileHandler

from app.config import settings


LOG_DIR = os.getenv(
    "LOG_DIR",
    "logs"
)

os.makedirs(
    LOG_DIR,
    exist_ok=True
)


def setup_logger():

    log_level = settings.LOG_LEVEL.upper()

    logger = logging.getLogger(
        "sentinel_scan"
    )

    logger.setLevel(
        log_level
    )


    # prevent duplicate handlers
    if logger.handlers:

        return logger


    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

    )


    # =====================
    # CONSOLE LOG
    # =====================

    console_handler = logging.StreamHandler(
        sys.stdout
    )

    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )


    # =====================
    # FILE LOG
    # =====================

    file_handler = RotatingFileHandler(

        f"{LOG_DIR}/sentinelscan.log",

        maxBytes=2_000_000,

        backupCount=3

    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )


    # =====================
    # QUIET NOISY LIBRARIES
    # =====================

    logging.getLogger(
        "urllib3"
    ).setLevel(logging.WARNING)

    logging.getLogger(
        "httpx"
    ).setLevel(logging.WARNING)

    logging.getLogger(
        "celery"
    ).setLevel(logging.INFO)

    logging.getLogger(
        "openai"
    ).setLevel(logging.WARNING)


    logger.info(
        "Logger initialized"
    )


    return logger    