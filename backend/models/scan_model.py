from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime

from app.database import Base


# =========================
# SCAN HISTORY TABLE
# =========================

class ScanHistory(Base):

    __tablename__ = "scan_history"


    # primary key
    id = Column(

        Integer,

        primary_key=True,

        index=True

    )


    # repository scanned
    repo = Column(

        String,

        nullable=False,

        index=True

    )


    # scan status
    status = Column(

        String,

        default="queued",

        index=True

    )


    # report reference
    report_id = Column(

        String,

        nullable=True

    )


    # issue count
    total_issues = Column(

        Integer,

        default=0

    )


    # severity breakdown
    severity_summary = Column(

        JSON,

        nullable=True

    )


    # timestamps
    created_at = Column(

        DateTime,

        default=datetime.utcnow

    )


    completed_at = Column(

        DateTime,

        nullable=True

    )


    # optional error message
    error_message = Column(

        String,

        nullable=True

    )


    # optional branch name
    branch = Column(

        String,

        nullable=True

    )


    # scan duration seconds
    duration = Column(

        Integer,

        nullable=True

    )