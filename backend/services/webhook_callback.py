import requests
import logging
import time
from typing import Dict

from app.config import settings


logger = logging.getLogger(
    "sentinel_scan.webhook"
)


# =========================
# CONFIG
# =========================

N8N_WEBHOOK_URL = getattr(

    settings,

    "N8N_WEBHOOK_URL",

    "http://localhost:5678/webhook/scan-result"

)

N8N_TOKEN = getattr(

    settings,

    "N8N_TOKEN",

    None

)


MAX_RETRIES = 3

TIMEOUT = 20


# =========================
# SEND RESULT TO N8N
# =========================

def notify_n8n(

    payload: Dict

) -> Dict:


    if not isinstance(

        payload,

        dict

    ):

        logger.error(

            "Invalid webhook payload"

        )

        return {

            "status": "invalid_payload"

        }


    headers = {

        "Content-Type":

        "application/json"

    }


    if N8N_TOKEN:

        headers["Authorization"] = (

            f"Bearer {N8N_TOKEN}"

        )


    logger.info(

        f"Sending results to n8n "

        f"url={N8N_WEBHOOK_URL}"

    )


    # =====================
    # RETRY LOOP
    # =====================

    for attempt in range(

        1,

        MAX_RETRIES + 1

    ):


        try:

            response = requests.post(

                N8N_WEBHOOK_URL,

                json=payload,

                headers=headers,

                timeout=TIMEOUT

            )


            response.raise_for_status()


            logger.info(

                f"n8n success "

                f"status={response.status_code} "

                f"attempt={attempt}"

            )


            return {

                "status": "sent",

                "http_status": response.status_code,

                "attempt": attempt

            }


        except requests.exceptions.Timeout:

            logger.warning(

                f"n8n timeout "

                f"attempt={attempt}"

            )


        except requests.exceptions.ConnectionError:

            logger.warning(

                f"n8n connection error "

                f"attempt={attempt}"

            )


        except requests.exceptions.HTTPError as e:

            logger.error(

                f"n8n http error "

                f"{response.status_code} "

                f"{response.text}"

            )


            return {

                "status": "http_error",

                "http_status": response.status_code

            }


        except Exception as e:

            logger.error(

                f"n8n unexpected error "

                f"{str(e)}"

            )


        # exponential backoff
        time.sleep(

            attempt * 2

        )


    return {

        "status": "failed",

        "attempts": MAX_RETRIES

    }    