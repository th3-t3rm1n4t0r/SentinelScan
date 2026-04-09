from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict
from datetime import datetime


# =========================
# REQUEST SCHEMA
# =========================

class ScanRequest(BaseModel):

    repo_url: HttpUrl

    branch: Optional[str] = None


# =========================
# FINDING SCHEMA
# =========================

class Finding(BaseModel):

    file: str

    issue: str

    severity: str

    line: Optional[int]

    snippet: Optional[str]


# =========================
# AI FIX SCHEMA
# =========================

class FixSuggestion(BaseModel):

    file: Optional[str]

    issue: str

    severity: Optional[str]

    fix: Optional[str]

    explanation: Optional[str]


# =========================
# REPORT SUMMARY
# =========================

class SeveritySummary(BaseModel):

    Critical: int = 0

    High: int = 0

    Medium: int = 0

    Low: int = 0


class ReportSummary(BaseModel):

    total_issues: int

    severity: SeveritySummary


# =========================
# REPORT RESPONSE
# =========================

class ReportResponse(BaseModel):

    report_id: str

    repo: str

    generated_at: Optional[str]

    summary: ReportSummary

    findings: List[Finding]

    fixes: List[FixSuggestion]


# =========================
# TASK RESPONSE
# =========================

class TaskResponse(BaseModel):

    status: str

    task_id: Optional[str] = None

    message: Optional[str] = None

    result: Optional[Dict] = None


# =========================
# SCAN HISTORY RESPONSE
# =========================

class ScanHistoryResponse(BaseModel):

    id: int

    repo: str

    status: str

    report_id: Optional[str]

    total_issues: int

    severity_summary: Optional[Dict]

    created_at: datetime

    completed_at: Optional[datetime]

    duration: Optional[int]


    class Config:

        orm_mode = True