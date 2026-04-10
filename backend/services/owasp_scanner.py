import re
from typing import List, Dict


# =============================
# SQL Injection Detection
# =============================
# Detect ONLY unsafe string building in SQL queries
# Ignore parameterized queries (%s, ?, :param)

SQL_INJECTION_PATTERN = re.compile(
    r"""
    (SELECT|INSERT|UPDATE|DELETE)     # SQL keywords
    .*                                # anything
    (
        \+                            # string concat
        | f["']                       # f-string
        | \%                          # % formatting
        | \.format\(                  # .format()
    )
    .*                                # anything
    (input\(|request\.|params\[|form\[)
    """,
    re.IGNORECASE | re.VERBOSE,
)


def detect_sql_injection(code: str):

    if SQL_INJECTION_PATTERN.search(code):

        return {
            "type": "SQL Injection",
            "severity": "HIGH",
            "message": "SQL query built using string concatenation",
        }

    return None


# =============================
# Insecure HTTP Detection
# =============================
# flag only real external HTTP APIs
# ignore localhost, w3.org, xml schemas

INSECURE_HTTP_PATTERN = re.compile(
    r"""
    http://
    (?!localhost|127\.0\.0\.1|0\.0\.0\.0)
    (?!www\.w3\.org)
    (?!schemas\.xmlsoap\.org)
    (?!xmlns)
    [a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}
    """,
    re.IGNORECASE | re.VERBOSE,
)


def detect_insecure_http(code: str):

    if INSECURE_HTTP_PATTERN.search(code):

        return {
            "type": "Insecure HTTP",
            "severity": "MEDIUM",
            "message": "External API using HTTP instead of HTTPS",
        }

    return None


# =============================
# Optional extra OWASP checks
# =============================

HARDCODED_SECRET_PATTERN = re.compile(
    r"(API_KEY|SECRET|PASSWORD)\s*=\s*['\"].+['\"]",
    re.IGNORECASE,
)

def detect_secrets(code: str):

    if HARDCODED_SECRET_PATTERN.search(code):

        return {
            "type": "Hardcoded Secret",
            "severity": "HIGH",
            "message": "Possible hardcoded credential",
        }

    return None


# =============================
# Optimize results before AI
# =============================

def optimize_results(findings: List[Dict]):

    # remove duplicates
    unique = {}

    for f in findings:

        key = f["type"] + f["message"]

        unique[key] = f

    findings = list(unique.values())

    # send only important issues to OpenAI
    IMPORTANT = ["HIGH", "CRITICAL"]

    findings = [f for f in findings if f["severity"] in IMPORTANT]

    # limit results (prevent token overflow)
    MAX_RESULTS = 15

    return findings[:MAX_RESULTS]


# =============================
# Main scan function
# =============================

def scan_code(code: str):

    findings = []

    sql_issue = detect_sql_injection(code)
    if sql_issue:
        findings.append(sql_issue)

    http_issue = detect_insecure_http(code)
    if http_issue:
        findings.append(http_issue)

    secret_issue = detect_secrets(code)
    if secret_issue:
        findings.append(secret_issue)

    return optimize_results(findings) 