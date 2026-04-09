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

    task_default_retry_delay=15,

    task_annotations={

        "*": {

            "max_retries": 3

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

        "workers.scan_tasks.run_scan": {

            "queue": "scan_queue"

        }

    },


    # -----------------
    # worker performance
    # -----------------

    worker_concurrency=4,

    worker_disable_rate_limits=True,


    # -----------------
    # memory protection
    # -----------------

    worker_max_tasks_per_child=30,

    worker_max_memory_per_child=200000,   # 200MB


    # -----------------
    # time limits
    # -----------------

    task_soft_time_limit=360,   # graceful stop

    task_time_limit=420,        # hard stop


    # -----------------
    # connection stability
    # -----------------

    broker_connection_retry_on_startup=True,

    broker_connection_max_retries=10,

)


# =========================
# DEFAULT QUEUE
# =========================

celery.conf.task_default_queue = "scan_queue"

celery.conf.task_default_exchange = "scan"

celery.conf.task_default_routing_key = "scan.default"


# =========================
# OPTIONAL DEBUG
# =========================

if settings.DEBUG:

    celery.conf.update(

        task_always_eager=False,

        worker_send_task_events=True

    )


# =========================
# STARTUP LOG
# =========================

logger.info(
    "Celery worker ready"
)   