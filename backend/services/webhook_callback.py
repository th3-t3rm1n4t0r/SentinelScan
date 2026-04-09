import requests
import logging
from typing import Dict, Optional

from app.config import settings


logger = logging.getLogger(
    "sentinel_scan.webhook_callback"
)


# =========================
# CONFIG
# =========================

N8N_WEBHOOK_URL = settings.__dict__.get(

    "N8N_WEBHOOK_URL",

    "http://localhost:5678/webhook/scan-result"

)

N8N_TOKEN = settings.__dict__.get(

    "N8N_TOKEN",

    None

)


MAX_RETRIES = 3

TIMEOUT = 20


# =========================
# SEND RESULT TO N8N
# =========================

def notify_n8n(

    data: Dict

) -> Dict:


    if not isinstance(data, dict):

        logger.error(

            "invalid webhook payload"

        )

        return {

            "status": "invalid_payload"

        }


    headers = {

        "Content-Type": "application/json"

    }


    if N8N_TOKEN:

        headers["Authorization"] = (

            f"Bearer {N8N_TOKEN}"

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

                json=data,

                headers=headers,

                timeout=TIMEOUT

            )


            response.raise_for_status()


            logger.info(

                f"n8n success | "
                f"attempt={attempt} | "
                f"status={response.status_code}"

            )


            return {

                "status": "sent",

                "http_status": response.status_code,

                "attempt": attempt

            }


        except requests.exceptions.Timeout:

            logger.warning(

                f"n8n timeout attempt={attempt}"

            )


        except requests.exceptions.HTTPError:

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

                f"n8n error attempt={attempt} "

                f"{str(e)}"

            )


    return {

        "status": "failed",

        "attempts": MAX_RETRIES

    }