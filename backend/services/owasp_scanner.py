
import re
import logging
from typing import List, Dict


logger = logging.getLogger(
    "sentinel_scan.owasp"
)


# =========================
# OWASP PATTERNS
# =========================

OWASP_PATTERNS = {

    "SQL_INJECTION":

        re.compile(
            r"(SELECT|INSERT|UPDATE|DELETE).*?(\+|\%s|\{)",
            re.IGNORECASE
        ),


    "COMMAND_INJECTION":

        re.compile(
            r"os\.system|subprocess\.Popen|subprocess\.call|eval\(",
            re.IGNORECASE
        ),


    "PATH_TRAVERSAL":

        re.compile(
            r"\.\./"
        ),


    "HARDCODED_PASSWORD":

        re.compile(
            r"(password|passwd|pwd)\s*=\s*[\"'].*?[\"']",
            re.IGNORECASE
        ),


    "SECRET_KEY":

        re.compile(
            r"(secret|token|api_key)\s*=\s*[\"'][A-Za-z0-9_\-]{16,}[\"']",
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


    "DEBUG_TRUE":

        re.compile(
            r"DEBUG\s*=\s*True"
        ),


    "SSRF_RISK":

        re.compile(
            r"requests\.(get|post)\(.+input",
            re.IGNORECASE
        ),


    "EVAL_USAGE":

        re.compile(
            r"\beval\("
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

    "JWT_TOKEN": "medium",

    "PATH_TRAVERSAL": "medium",

    "SSRF_RISK": "medium",

    "EVAL_USAGE": "high",

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

        f"findings total={len(findings)}"

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

        sev = f["severity"]

        summary[sev] += 1


    return summary