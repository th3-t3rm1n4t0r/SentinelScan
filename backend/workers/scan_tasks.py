from workers.celery_worker import celery

import logging
from datetime import datetime

from services.github_tree_service import get_repo_tree
from services.owasp_scanner import scan_files, summarize_findings
from services.ai_service import ai_fix
from services.report_service import create_report
from services.webhook_service import notify_n8n

from services.pii_scrubber import mask_pii
from services.context_selector import select_relevant_files
from services.github_pr_service import create_fix_pr

from models.scan_history import ScanHistory
from app.database import SessionLocal


logger = logging.getLogger(
    "sentinel_scan.worker"
)


# =========================
# CELERY TASK
# =========================

@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3}
)

def run_scan(

    self,

    repo_url: str,

    issue_text: str = "",

    issue_number: int = 0

):

    db = SessionLocal()

    start_time = datetime.utcnow()

    task_id = self.request.id


    logger.info(

        f"scan started "

        f"repo={repo_url} "

        f"task={task_id}"

    )


    # =====================
    # CREATE DB RECORD
    # =====================

    scan_record = ScanHistory(

        task_id=task_id,

        repo=repo_url,

        status="running",

        scan_type="repo",

        created_at=start_time

    )

    db.add(scan_record)

    db.commit()


    try:

        # =====================
        # FETCH REPO FILES
        # =====================

        all_files = get_repo_tree(

            repo_url

        )


        logger.info(

            f"files fetched={len(all_files)}"

        )


        # =====================
        # CONTEXT FILTER
        # =====================

        paths = [

            f["path"]

            for f in all_files

        ]


        selected_paths = select_relevant_files(

            issue_text,

            paths

        ) if issue_text else paths


        files = [

            f for f in all_files

            if f["path"] in selected_paths

        ]


        logger.info(

            f"context files={len(files)}"

        )


        # =====================
        # PII SCRUB
        # =====================

        for f in files:

            f["content"] = mask_pii(

                f.get("content", "")

            )


        # =====================
        # OWASP SCAN
        # =====================

        findings = scan_files(

            files

        )


        severity_summary = summarize_findings(

            findings

        )


        logger.info(

            f"findings={len(findings)}"

        )


        # =====================
        # AI FIX
        # =====================

        fixes = ai_fix(

            findings

        )


        # =====================
        # CREATE PR
        # =====================

        pr_url = None


        if fixes:

            try:

                pr_url = create_fix_pr(

                    repo_url,

                    fixes

                )

            except Exception as e:

                logger.warning(

                    f"PR creation failed {str(e)}"

                )


        # =====================
        # CREATE REPORT
        # =====================

        report = create_report(

            findings=findings,

            fixes=fixes,

            repo=repo_url

        )


        report["pull_request"] = pr_url


        # =====================
        # UPDATE DB RECORD
        # =====================

        end_time = datetime.utcnow()


        scan_record.status = "completed"

        scan_record.report_id = report["report_id"]

        scan_record.total_issues = len(findings)

        scan_record.severity_summary = severity_summary

        scan_record.completed_at = end_time

        scan_record.duration = int(

            (end_time - start_time)

            .total_seconds()

        )


        db.commit()


        # =====================
        # WEBHOOK CALLBACK
        # =====================

        webhook_payload = {

            "task_id": task_id,

            "repo_url": repo_url,

            "issue_number": issue_number,

            "summary": report["summary"],

            "report": report,

            "pull_request": pr_url,

            "status": "completed"

        }


        notify_n8n(

            webhook_payload

        )


        logger.info(

            f"scan completed "

            f"task={task_id}"

        )


        return webhook_payload


    except Exception as e:


        logger.error(

            f"scan failed "

            f"task={task_id} "

            f"{str(e)}"

        )


        scan_record.status = "failed"

        scan_record.error_message = str(e)


        scan_record.completed_at = datetime.utcnow()


        db.commit()


        notify_n8n({

            "task_id": task_id,

            "repo_url": repo_url,

            "status": "failed",

            "error": str(e)

        })


        raise self.retry(exc=e)


    finally:

        db.close()   