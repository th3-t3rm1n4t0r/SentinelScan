from workers.celery_worker import celery

from services.github_service import clone_repo
from services.security_scanner import scan_files
from services.ai_service import ai_fix
from services.report_service import create_report

from models.scan_history import ScanHistory
from app.database import SessionLocal

from services.webhook_service import notify_n8n   

# =========================
# LOGGER
# =========================

logger = logging.getLogger(
    "sentinel_scan.worker.scan"
)


# =========================
# CELERY TASK
# =========================

@celery.task(
    bind=True,
    name="run_scan"
)

def run_scan(

    self,

    repo_url: str,

    issue_text: str = "",

    issue_number: int = 0

):

    db = SessionLocal()

    try:

        logger.info(
            f"Starting scan repo={repo_url}"
        )

        # -------------------------
        # CLONE REPOSITORY
        # -------------------------

        files = clone_repo(
            repo_url
        )


        # -------------------------
        # RUN SECURITY SCAN
        # -------------------------

        findings = scan_files(
            files
        )


        # -------------------------
        # AI FIX SUGGESTIONS
        # -------------------------

        fixes = ai_fix(
            findings
        )


        # -------------------------
        # CREATE REPORT
        # -------------------------

        report_path = create_report(

            findings,

            fixes

        )


        # -------------------------
        # SAVE HISTORY
        # -------------------------

        history = ScanHistory(

            repo_url=repo_url,

            issues_found=len(
                findings
            ),

            report_path=report_path

        )

        db.add(
            history
        )

        db.commit()


        # -------------------------
        # WEBHOOK NOTIFY
        # -------------------------

        notify_n8n(

            repo_url=repo_url,

            issues=len(findings),

            report=report_path

        )


        logger.info(
            f"Scan completed repo={repo_url}"
        )


        return {

            "repo": repo_url,

            "issues_found": len(findings),

            "report": report_path

        }


    except Exception as e:

        logger.exception(
            "scan failed"
        )

        raise e


    finally:

        db.close()  