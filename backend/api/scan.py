from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from celery.result import AsyncResult
import logging

from workers.scan_tasks import run_scan
from workers.celery_worker import celery


# =========================
# LOGGER
# =========================

logger = logging.getLogger(
    "sentinel_scan.api"
)


router = APIRouter(
    prefix="/scan",
    tags=["Security Scan"]
)


# =========================
# REQUEST MODEL
# =========================

class ScanRequest(BaseModel):

    repo_url: HttpUrl | None = None

    repository_owner: str | None = None

    repository_name: str | None = None

    issue_number: int | None = None


# =========================
# START SCAN
# =========================

@router.post("/github")

def scan_github(request: ScanRequest):

    try:

        # ---------- build repo url ----------

        if request.repo_url:

            repo_url = str(request.repo_url)

        elif request.repository_owner and request.repository_name:

            repo_url = f"https://github.com/{request.repository_owner}/{request.repository_name}"

        else:

            raise HTTPException(

                status_code=400,

                detail="Provide repo_url OR repository_owner + repository_name"

            )


        # ---------- normalize issue number ----------

        issue_number = request.issue_number or 0


        logger.info(

            f"Scan requested for {repo_url} issue {issue_number}"
        )


        # ---------- start celery task ----------

        task = run_scan.delay(

            repo_url,

            issue_number

        )


        return {

            "status": "queued",

            "task_id": task.id,

            "repo_url": repo_url,

            "issue_number": issue_number,

            "message": "Scan started successfully"

        }


    except Exception as e:

        logger.exception("Failed to start scan")

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# =========================
# CHECK TASK STATUS
# =========================

@router.get("/status/{task_id}")

def scan_status(task_id: str):

    task_result = AsyncResult(

        task_id,

        app=celery

    )


    state = task_result.state


    logger.info(

        f"Task {task_id} status {state}"
    )


    # ---------- celery states ----------

    if state == "PENDING":

        return {

            "status": "pending",

            "message": "Task waiting in queue"

        }


    elif state == "STARTED":

        return {

            "status": "running",

            "message": "Scan in progress"

        }


    elif state == "SUCCESS":

        return {

            "status": "completed",

            "result": task_result.result

        }


    elif state == "FAILURE":

        return {

            "status": "failed",

            "error": str(task_result.result)

        }


    return {

        "status": state

    }   