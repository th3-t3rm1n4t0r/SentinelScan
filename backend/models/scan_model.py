from sqlalchemy import Column, Integer, String, DateTime, JSON, func
from datetime import datetime

from app.database import Base


# =========================
# SCAN HISTORY TABLE
# =========================

class ScanHistory(Base):

    __tablename__ = "scan_history"


    # =========================
    # PRIMARY KEY
    # =========================

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    # =========================
    # CELERY TASK LINK
    # =========================

    task_id = Column(

        String,

        unique=True,

        index=True,

        nullable=False

    )


    # =========================
    # REPOSITORY INFO
    # =========================

    repo = Column(

        String,

        nullable=False,

        index=True

    )


    branch = Column(

        String,

        nullable=True

    )


    scan_type = Column(

        String,

        default="repo"  # repo | pull_request | webhook

    )


    # =========================
    # STATUS
    # =========================

    status = Column(

        String,

        default="queued",

        index=True

    )


    # =========================
    # RESULTS
    # =========================

    report_id = Column(

        String,

        nullable=True,

        index=True

    )


    total_issues = Column(

        Integer,

        default=0

    )


    severity_summary = Column(

        JSON,

        nullable=True,

        default=dict

    )


    # =========================
    # ERROR TRACKING
    # =========================

    error_message = Column(

        String,

        nullable=True

    )


    # =========================
    # TIMESTAMPS
    # =========================

    created_at = Column(

        DateTime(timezone=True),

        server_default=func.now()

    )


    completed_at = Column(

        DateTime(timezone=True),

        nullable=True

    )


    duration = Column(

        Integer,

        nullable=True

    )


    # =========================
    # HELPER METHOD
    # =========================

    def mark_completed(self):

        self.completed_at = datetime.utcnow()

        if self.created_at:

            self.duration = int(

                (
                    self.completed_at -

                    self.created_at

                ).total_seconds()

            )  