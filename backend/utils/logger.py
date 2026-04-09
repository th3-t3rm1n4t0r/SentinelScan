import logging
import sys
import os

from logging.handlers import RotatingFileHandler

from app.config import settings


# =========================
# CONFIG
# =========================

LOG_DIR = os.getenv(

    "LOG_DIR",

    "logs"

)

os.makedirs(

    LOG_DIR,

    exist_ok=True

)


LOG_FILE = os.path.join(

    LOG_DIR,

    "sentinelscan.log"

)


DEFAULT_LEVEL = "INFO"


# =========================
# SETUP LOGGER
# =========================

def setup_logger():

    level_name = getattr(

        settings,

        "LOG_LEVEL",

        DEFAULT_LEVEL

    )


    log_level = getattr(

        logging,

        str(level_name).upper(),

        logging.INFO

    )


    logger = logging.getLogger(

        "sentinel_scan"

    )


    logger.setLevel(

        log_level

    )


    logger.propagate = False


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


    console_handler.setLevel(

        log_level

    )


    console_handler.setFormatter(

        formatter

    )


    logger.addHandler(

        console_handler

    )


    # =====================
    # FILE LOG (ROTATING)
    # =====================

    file_handler = RotatingFileHandler(

        LOG_FILE,

        maxBytes=2_000_000,

        backupCount=5,

        encoding="utf-8"

    )


    file_handler.setLevel(

        log_level

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


    logging.getLogger(

        "asyncio"

    ).setLevel(logging.WARNING)


    logger.info(

        "Logger initialized"

    )


    return logger  