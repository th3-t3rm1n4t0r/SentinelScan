from pydantic import BaseModel, HttpUrl, Field, model_validator
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


# =========================
# ENUMS
# =========================

class SeverityLevel(str, Enum):

    critical = "critical"

    high = "high"

    medium = "medium"

    low = "low"


class ScanStatus(str, Enum):

    pending = "pending"

    running = "running"

    completed = "completed"

    failed = "failed"


# =========================
# REQUEST SCHEMA
# =========================

class ScanRequest(BaseModel):

    repo_url: Optional[HttpUrl] = Field(

        default=None,

        description="Full GitHub repository URL"

    )

    repository_owner: Optional[str] = Field(

        default=None,

        description="GitHub owner/org"

    )

    repository_name: Optional[str] = Field(

        default=None,

        description="Repository name"

    )

    branch: Optional[str] = Field(

        default="main",

        description="Branch name"

    )

    issue_number: Optional[int] = Field(

        default=None,

        description="GitHub issue reference"

    )


    @model_validator(mode="after")

    def validate_repo_input(self):

        if not self.repo_url and not (

            self.repository_owner and self.repository_name

        ):

            raise ValueError(

                "Provide repo_url OR repository_owner + repository_name"

            )

        return self


# =========================
# FINDING SCHEMA
# =========================

class Finding(BaseModel):

    file: str = Field(

        description="File path"

    )

    issue: str = Field(

        description="Type of vulnerability"

    )

    severity: SeverityLevel

    line: Optional[int] = Field(

        default=None,

        description="Line number"

    )

    snippet: Optional[str] = Field(

        default=None,

        description="Code snippet"

    )


# =========================
# AI FIX SCHEMA
# =========================

class FixSuggestion(BaseModel):

    file: Optional[str] = None

    issue: str

    severity: SeverityLevel

    fix: Optional[str] = None

    explanation: Optional[str] = None


# =========================
# REPORT SUMMARY
# =========================

class SeveritySummary(BaseModel):

    critical: int = 0

    high: int = 0

    medium: int = 0

    low: int = 0


class ReportSummary(BaseModel):

    total_issues: int

    severity: SeveritySummary


# =========================
# REPORT RESPONSE
# =========================

class ReportResponse(BaseModel):

    report_id: str

    repo: str

    branch: Optional[str] = None

    generated_at: datetime

    summary: ReportSummary

    findings: List[Finding]

    fixes: List[FixSuggestion]


# =========================
# TASK RESPONSE
# =========================

class TaskResponse(BaseModel):

    status: ScanStatus

    task_id: Optional[str] = None

    message: Optional[str] = None

    result: Optional[Dict] = None


# =========================
# SCAN HISTORY RESPONSE
# =========================

class ScanHistoryResponse(BaseModel):

    id: int

    task_id: str

    repo: str

    branch: Optional[str] = None

    scan_type: Optional[str] = None

    status: ScanStatus

    report_id: Optional[str] = None

    total_issues: int

    severity_summary: Optional[Dict] = None

    created_at: datetime

    completed_at: Optional[datetime] = None

    duration: Optional[int] = None

    error_message: Optional[str] = None


    class Config:

        from_attributes = True   # Pydantic v2 ORM support      