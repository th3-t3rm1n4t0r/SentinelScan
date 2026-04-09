import re
import logging
from typing import List, Dict


logger = logging.getLogger("sentinel_scan.owasp")


# =========================
# OWASP PATTERNS
# =========================

OWASP_PATTERNS = {

    # Injection
    "SQL_INJECTION":

        re.compile(
            r"(SELECT|INSERT|UPDATE|DELETE|WHERE).*(\+|%s|f\"|\{)",
            re.IGNORECASE
        ),

    "COMMAND_INJECTION":

        re.compile(
            r"os\.system|subprocess\.Popen|subprocess\.call|shell=True",
            re.IGNORECASE
        ),

    "EVAL_USAGE":

        re.compile(
            r"\beval\(|\bexec\(",
            re.IGNORECASE
        ),


    # Authentication & Secrets
    "HARDCODED_PASSWORD":

        re.compile(
            r"(password|passwd|pwd)\s*=\s*[\"'].*?[\"']",
            re.IGNORECASE
        ),

    "SECRET_KEY":

        re.compile(
            r"(secret|token|api[_-]?key)\s*=\s*[\"'][A-Za-z0-9_\-]{12,}[\"']",
            re.IGNORECASE
        ),

    "PRIVATE_KEY":

        re.compile(
            r"-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----"
        ),

    "JWT_TOKEN":

        re.compile(
            r"eyJ[A-Za-z0-9_-]+?\.[A-Za-z0-9_-]+?\.[A-Za-z0-9_-]+"
        ),

    "AWS_KEY":

        re.compile(
            r"AKIA[0-9A-Z]{16}"
        ),


    # File access risks
    "PATH_TRAVERSAL":

        re.compile(
            r"\.\./|\.\.\\"
        ),


    # Configuration issues
    "DEBUG_TRUE":

        re.compile(
            r"DEBUG\s*=\s*True"
        ),

    "INSECURE_HTTP":

        re.compile(
            r"http://"
        ),


    # SSRF risk
    "SSRF_RISK":

        re.compile(
            r"requests\.(get|post|put|delete)\(.+(input|request)",
            re.IGNORECASE
        ),


    # Deserialization risk
    "PICKLE_USAGE":

        re.compile(
            r"pickle\.loads|yaml\.load\(",
            re.IGNORECASE
        ),


    # CORS risk
    "CORS_ALLOW_ALL":

        re.compile(
            r"Access-Control-Allow-Origin.*\*"
        ),

}


# =========================
# SEVERITY MAP
# =========================

SEVERITY_MAP = {

    "SQL_INJECTION": "critical",

    "COMMAND_INJECTION": "critical",

    "PRIVATE_KEY": "critical",

    "AWS_KEY": "critical",

    "SECRET_KEY": "high",

    "HARDCODED_PASSWORD": "high",

    "EVAL_USAGE": "high",

    "PICKLE_USAGE": "high",

    "JWT_TOKEN": "medium",

    "PATH_TRAVERSAL": "medium",

    "SSRF_RISK": "medium",

    "INSECURE_HTTP": "medium",

    "CORS_ALLOW_ALL": "medium",

    "DEBUG_TRUE": "low"

}


# =========================
# MAIN SCANNER
# =========================

def scan_files(

    files: List[Dict]

) -> List[Dict]:

    findings = []


    for file in files:

        content = file.get(

            "content",

            ""

        )

        path = file.get(

            "path",

            "unknown"

        )


        if not content:

            continue


        lines = content.splitlines()


        for i, line in enumerate(

            lines,

            start=1

        ):

            for vuln, pattern in OWASP_PATTERNS.items():

                if pattern.search(line):

                    findings.append({

                        "file": path,

                        "issue": vuln,

                        "severity": SEVERITY_MAP.get(

                            vuln,

                            "low"

                        ),

                        "line": i,

                        "snippet": line.strip()[:200]

                    })


    logger.info(

        f"OWASP findings total={len(findings)}"

    )


    return findings


# =========================
# SUMMARY HELPER
# =========================

def summarize_findings(

    findings: List[Dict]

):

    summary = {

        "critical": 0,

        "high": 0,

        "medium": 0,

        "low": 0

    }


    for f in findings:

        sev = f.get(

            "severity",

            "low"

        )


        if sev not in summary:

            summary[sev] = 0


        summary[sev] += 1


    return summary  