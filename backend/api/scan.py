from fastapi import APIRouter, HTTPException, Depends, status
from celery.result import AsyncResult
import logging

from workers.scan_tasks import run_scan
from workers.celery_worker import celery

from app.schemas import (
    ScanRequest,
    TaskResponse
)

from app.dependencies import verify_api_key


# =========================
# LOGGER
# =========================

logger = logging.getLogger(
    "sentinel_scan.api.scan"
)


# =========================
# ROUTER
# =========================

router = APIRouter(
    prefix="/scan",
    tags=["Security Scan"]
)


# =========================
# START SCAN
# =========================

@router.post(

    "/github",

    response_model=TaskResponse,

    dependencies=[Depends(verify_api_key)]

)

def scan_github(

    request: ScanRequest

):

    try:

        # -------------------------
        # BUILD REPO URL
        # -------------------------

        if request.repo_url:

            repo_url = str(

                request.repo_url

            )

        elif (

            request.repository_owner

            and

            request.repository_name

        ):

            repo_url = (

                f"https://github.com/"

                f"{request.repository_owner}/"

                f"{request.repository_name}"

            )

        else:

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Provide repo_url OR owner + repo"

            )


        issue_number = request.issue_number or 0


        logger.info(

            f"scan requested repo={repo_url}"

        )


        # -------------------------
        # START CELERY TASK
        # -------------------------

        task = run_scan.delay(

            repo_url,

            "",          # issue text optional

            issue_number

        )


        return TaskResponse(

            status="pending",

            task_id=task.id,

            message="Scan started"

        )


    except HTTPException:

        raise


    except Exception as e:

        logger.exception(

            "scan start failed"

        )


        raise HTTPException(

            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,

            detail=str(e)

        )


# =========================
# TASK STATUS
# =========================

@router.get(

    "/status/{task_id}",

    response_model=TaskResponse,

    dependencies=[Depends(verify_api_key)]

)

def scan_status(

    task_id: str

):

    task_result = AsyncResult(

        task_id,

        app=celery

    )


    state = task_result.state


    logger.info(

        f"task status task={task_id} state={state}"

    )


    if state == "PENDING":

        return TaskResponse(

            status="pending",

            task_id=task_id,

            message="Waiting in queue"

        )


    elif state == "STARTED":

        return TaskResponse(

            status="running",

            task_id=task_id,

            message="Scan in progress"

        )


    elif state == "SUCCESS":

        return TaskResponse(

            status="completed",

            task_id=task_id,

            result=task_result.result

        )


    elif state == "FAILURE":

        return TaskResponse(

            status="failed",

            task_id=task_id,

            message=str(task_result.result)

        )


    return TaskResponse(

        status=state,

        task_id=task_id

    ) 