from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    func,
    Index
)

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

        String(120),

        unique=True,

        index=True,

        nullable=False

    )


    # =========================
    # REPOSITORY INFO
    # =========================

    repo = Column(

        String(300),

        nullable=False,

        index=True

    )


    branch = Column(

        String(120),

        nullable=True,

        index=True

    )


    scan_type = Column(

        String(50),

        default="repo",   # repo | pull_request | webhook

        index=True

    )


    # =========================
    # STATUS
    # =========================

    status = Column(

        String(50),

        default="queued",

        index=True

    )


    # =========================
    # RESULTS
    # =========================

    report_id = Column(

        String(80),

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

        String(2000),

        nullable=True

    )


    # =========================
    # TIMESTAMPS
    # =========================

    created_at = Column(

        DateTime(timezone=True),

        server_default=func.now(),

        index=True

    )


    completed_at = Column(

        DateTime(timezone=True),

        nullable=True,

        index=True

    )


    duration = Column(

        Integer,

        nullable=True

    )


    # =========================
    # INDEXES
    # =========================

    __table_args__ = (

        Index("idx_repo_status", "repo", "status"),

        Index("idx_task_status", "task_id", "status"),

    )


    # =========================
    # HELPER METHODS
    # =========================

    def mark_running(self):

        self.status = "running"


    def mark_completed(self):

        self.status = "completed"

        self.completed_at = datetime.utcnow()

        self.calculate_duration()


    def mark_failed(self, error: str):

        self.status = "failed"

        self.error_message = error

        self.completed_at = datetime.utcnow()

        self.calculate_duration()


    def calculate_duration(self):

        if self.created_at and self.completed_at:

            self.duration = int(

                (

                    self.completed_at -

                    self.created_at

                ).total_seconds()

            ) 