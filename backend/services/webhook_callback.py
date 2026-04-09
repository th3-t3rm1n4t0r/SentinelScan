import requests
import logging
import time

from typing import Dict, Any

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

MAX_RETRIES = getattr(

    settings,

    "WEBHOOK_RETRIES",

    3

)

TIMEOUT = getattr(

    settings,

    "WEBHOOK_TIMEOUT",

    20

)


# =========================
# SEND RESULT TO N8N
# =========================

def notify_n8n(

    payload: Dict[str, Any]

) -> Dict:


    if not isinstance(payload, dict):

        logger.error(

            "Webhook payload must be dict"

        )

        return {

            "status": "invalid_payload"

        }


    if not payload:

        logger.warning(

            "Webhook payload empty"

        )


    headers = {

        "Content-Type":

        "application/json"

    }


    if N8N_TOKEN:

        headers["Authorization"] = (

            f"Bearer {N8N_TOKEN}"

        )


    logger.info(

        f"Sending scan result to n8n "

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


            # retry on 5xx errors
            if response.status_code >= 500:

                raise requests.exceptions.HTTPError(

                    f"Server error {response.status_code}"

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

                f"attempt={attempt} "

                f"{str(e)}"

            )


            # 4xx usually should not retry
            if response.status_code < 500:

                return {

                    "status": "http_error",

                    "http_status": response.status_code,

                    "response": safe_text(response)

                }


        except Exception as e:

            logger.error(

                f"n8n unexpected error "

                f"{str(e)}"

            )


        # exponential backoff
        sleep_time = attempt * 2

        logger.info(

            f"retrying in {sleep_time}s..."

        )

        time.sleep(

            sleep_time

        )


    logger.error(

        "n8n webhook failed after retries"

    )


    return {

        "status": "failed",

        "attempts": MAX_RETRIES

    }


# =========================
# SAFE RESPONSE TEXT
# =========================

def safe_text(response):

    try:

        return response.text[:500]

    except Exception:

        return ""   
    
    
    
    