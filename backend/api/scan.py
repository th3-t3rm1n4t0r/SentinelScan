
from fastapi import APIRouter
from services.github_service import clone_repo
from services.security_scanner import scan_code
from services.ai_service import ai_fix
from services.report_service import create_report

router = APIRouter(prefix="/scan")

@router.post("/github")
def scan_github(data: dict):
    repo_url = data["repo_url"]

    path = clone_repo(repo_url)

    vulnerabilities = scan_code(path)

    fixes = ai_fix(vulnerabilities)

    report = create_report(vulnerabilities)

    return {
        "vulnerabilities": vulnerabilities,
        "fixes": fixes,
        "report": report
    }
