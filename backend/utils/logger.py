import logging
import sys

from app.config import settings


def setup_logger():

    log_level = settings.LOG_LEVEL.upper()


    logging.basicConfig(

        level=log_level,

        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",

        handlers=[

            logging.StreamHandler(sys.stdout)

        ]

    )


    # reduce noisy logs
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logging.getLogger("celery").setLevel(logging.INFO)

    logging.getLogger("openai").setLevel(logging.WARNING)


    logger = logging.getLogger("sentinel_scan")

    logger.info("Logger initialized")


    return logger