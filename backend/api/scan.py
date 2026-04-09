from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult

from workers.scan_tasks import run_scan
from workers.celery_worker import celery


router = APIRouter()


# =========================
# REQUEST MODEL
# =========================

class ScanRequest(BaseModel):

    repo_url: str


# =========================
# START SCAN
# =========================

@router.post("/github")

def scan_github(

    request: ScanRequest

):

    if not request.repo_url:

        raise HTTPException(

            status_code=400,

            detail="repo_url required"

        )


    task = run_scan.delay(

        request.repo_url

    )


    return {

        "status": "queued",

        "task_id": task.id,

        "message": "scan started"

    }


# =========================
# CHECK TASK STATUS
# =========================

@router.get("/status/{task_id}")

def scan_status(

    task_id: str

):

    task_result = AsyncResult(

        task_id,

        app=celery

    )


    if task_result.state == "PENDING":

        return {

            "status": "pending"

        }


    if task_result.state == "STARTED":

        return {

            "status": "running"

        }


    if task_result.state == "SUCCESS":

        return {

            "status": "completed",

            "result": task_result.result

        }


    if task_result.state == "FAILURE":

        return {

            "status": "failed",

            "error": str(

                task_result.result

            )

        }


    return {

        "status": task_result.state

    }