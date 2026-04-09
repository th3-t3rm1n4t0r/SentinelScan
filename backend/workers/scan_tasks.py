from workers.celery_worker import celery

import logging
from datetime import datetime

from services.github_tree_service import get_repo_tree
from services.owasp_scanner import scan_files
from services.ai_service import ai_fix
from services.report_service import create_report
from services.webhook_service import notify_n8n

from models.scan_model import ScanHistory
from app.database import SessionLocal


logger = logging.getLogger(
    "sentinel_scan.worker"
)


# =========================
# MAIN BACKGROUND TASK
# =========================

@celery.task(

    bind=True,

    autoretry_for=(Exception,),

    retry_backoff=True,

    retry_kwargs={

        "max_retries": 3

    }

)
def run_scan(

    self,

    repo_url: str

):

    db = SessionLocal()

    start_time = datetime.utcnow()

    logger.info(

        f"scan started | repo={repo_url}"

    )


    try:

        # =====================
        # 1. FETCH REPO FILES
        # =====================

        files = get_repo_tree(

            repo_url

        )

        logger.info(

            f"files fetched={len(files)}"

        )


        # =====================
        # 2. OWASP SCAN
        # =====================

        findings = scan_files(

            files

        )


        logger.info(

            f"findings={len(findings)}"

        )


        # =====================
        # 3. AI FIX SUGGESTIONS
        # =====================

        fixes = ai_fix(

            findings

        )


        # =====================
        # 4. CREATE REPORT
        # =====================

        report = create_report(

            findings=findings,

            fixes=fixes,

            repo=repo_url

        )


        # =====================
        # 5. STORE DB HISTORY
        # =====================

        scan_record = ScanHistory(

            repo=repo_url,

            status="completed",

            created_at=start_time

        )

        db.add(

            scan_record

        )

        db.commit()


        # =====================
        # 6. NOTIFY N8N
        # =====================

        webhook_payload = {

            "repo": repo_url,

            "report": report,

            "summary": report.get("summary")

        }


        notify_n8n(

            webhook_payload

        )


        logger.info(

            f"scan completed | repo={repo_url}"

        )


        return {

            "status": "completed",

            "repo": repo_url,

            "report": report

        }


    except Exception as e:

        logger.error(

            f"scan failed | {str(e)}"

        )


        # store failure
        scan_record = ScanHistory(

            repo=repo_url,

            status="failed",

            created_at=start_time

        )

        db.add(

            scan_record

        )

        db.commit()


        raise self.retry(

            exc=e

        )


    finally:

        db.close()