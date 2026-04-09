from celery import Celery
import logging

from app.config import settings


logger = logging.getLogger(
    "sentinel_scan.celery"
)


# =========================
# CELERY INSTANCE
# =========================

celery = Celery(

    "sentinelscan",

    broker=settings.REDIS_URL,

    backend=settings.REDIS_URL,

    include=[

        "workers.scan_tasks"

    ]

)


# =========================
# CONFIG
# =========================

celery.conf.update(

    # serialization
    task_serializer="json",

    result_serializer="json",

    accept_content=["json"],


    # timezone
    timezone="Asia/Kolkata",

    enable_utc=True,


    # reliability
    task_acks_late=True,

    worker_prefetch_multiplier=1,


    # retry strategy
    task_default_retry_delay=15,

    task_annotations={

        "*": {

            "max_retries": 3

        }

    },


    # tracking
    task_track_started=True,

    result_expires=3600,


    # routing queues
    task_routes={

        "workers.scan_tasks.run_scan": {

            "queue": "scan_queue"

        }

    },


    # performance tuning
    worker_concurrency=2,


    # memory protection
    worker_max_tasks_per_child=40,


    # task limits
    task_time_limit=300,

    task_soft_time_limit=240,

)


# =========================
# STARTUP LOG
# =========================

logger.info(

    "Celery worker configured"

)