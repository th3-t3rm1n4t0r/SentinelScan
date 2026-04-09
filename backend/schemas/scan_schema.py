from pydantic import BaseModel, HttpUrl, Field
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



# =========================
# REQUEST SCHEMA
# =========================

class ScanRequest(BaseModel):

    repo_url: Optional[HttpUrl] = None

    repository_owner: Optional[str] = None

    repository_name: Optional[str] = None

    branch: Optional[str] = None

    issue_number: Optional[int] = None



# =========================
# FINDING SCHEMA
# =========================

class Finding(BaseModel):

    file: str = Field(

        description="file path"

    )

    issue: str = Field(

        description="type of vulnerability"

    )

    severity: SeverityLevel

    line: Optional[int] = None

    snippet: Optional[str] = None



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

    status: str

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

    status: str

    report_id: Optional[str] = None

    total_issues: int

    severity_summary: Optional[Dict] = None

    created_at: datetime

    completed_at: Optional[datetime] = None

    duration: Optional[int] = None

    error_message: Optional[str] = None


    class Config:

        from_attributes = True   # replaces orm_mode in Pydantic v2   