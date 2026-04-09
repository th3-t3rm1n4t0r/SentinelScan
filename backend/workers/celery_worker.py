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
# CONFIGURATION
# =========================

celery.conf.update(

    # -----------------
    # serialization
    # -----------------

    task_serializer="json",

    result_serializer="json",

    accept_content=["json"],


    # -----------------
    # timezone
    # -----------------

    timezone="Asia/Kolkata",

    enable_utc=True,


    # -----------------
    # reliability
    # -----------------

    task_acks_late=True,

    task_reject_on_worker_lost=True,

    worker_prefetch_multiplier=1,


    # -----------------
    # retry behaviour
    # -----------------

    task_default_retry_delay=20,

    task_annotations={

        "*": {

            "max_retries": 3,

            "autoretry_for": (

                Exception,

            ),

            "retry_backoff": True,

            "retry_backoff_max": 120,

            "retry_jitter": True

        }

    },


    # -----------------
    # task tracking
    # -----------------

    task_track_started=True,

    result_expires=3600,


    # -----------------
    # queue routing
    # -----------------

    task_routes={

        "workers.scan_tasks": {
            "queue": "scan"
        }
    }

)