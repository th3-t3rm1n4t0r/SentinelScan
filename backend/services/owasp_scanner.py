import re
import logging
from typing import List, Dict

logger = logging.getLogger("sentinel_scan.owasp")


# =========================
# COMPILED PATTERNS
# =========================

PATTERNS = [

    {
        "name": "SQL Injection",
        "regex": r"(SELECT|INSERT|UPDATE|DELETE).*?\+.*",
        "severity": "High"
    },

    {
        "name": "XSS Script Tag",
        "regex": r"<script.*?>.*?</script>",
        "severity": "High"
    },

    {
        "name": "Command Injection",
        "regex": r"os\.system|subprocess\.Popen|subprocess\.call",
        "severity": "High"
    },

    {
        "name": "Eval Injection",
        "regex": r"\beval\s*\(",
        "severity": "High"
    },

    {
        "name": "Hardcoded Secret",
        "regex": r"(api[_-]?key|secret|token|password)\s*=\s*['\"]",
        "severity": "Critical"
    },

    {
        "name": "JWT Hardcoded Secret",
        "regex": r"jwt\.encode\(.+['\"]",
        "severity": "High"
    },

    {
        "name": "Debug Enabled",
        "regex": r"debug\s*=\s*True",
        "severity": "Medium"
    },

    {
        "name": "Weak Random",
        "regex": r"random\.random\(",
        "severity": "Medium"
    },

    {
        "name": "Weak Hash",
        "regex": r"hashlib\.md5|hashlib\.sha1",
        "severity": "High"
    },

    {
        "name": "Path Traversal",
        "regex": r"\.\./",
        "severity": "High"
    },

    {
        "name": "Open Redirect",
        "regex": r"redirect\(.+\+",
        "severity": "Medium"
    },

    {
        "name": "Pickle Deserialization",
        "regex": r"pickle\.loads",
        "severity": "Critical"
    },

    {
        "name": "Insecure Temp File",
        "regex": r"tempfile\.mktemp",
        "severity": "High"
    },

    {
        "name": "Dangerous YAML Load",
        "regex": r"yaml\.load\(",
        "severity": "High"
    },

    {
        "name": "Hardcoded Private Key",
        "regex": r"BEGIN RSA PRIVATE KEY",
        "severity": "Critical"
    },

    {
        "name": "Hardcoded AWS Key",
        "regex": r"AKIA[0-9A-Z]{16}",
        "severity": "Critical"
    },

    {
        "name": "Flask Debug Mode",
        "regex": r"app\.run\(.*debug\s*=\s*True",
        "severity": "High"
    },

    {
        "name": "Unsafe Deserialization",
        "regex": r"marshal\.loads|dill\.loads",
        "severity": "High"
    },

    {
        "name": "HTTP instead of HTTPS",
        "regex": r"http://",
        "severity": "Low"
    }

]


# precompile regex
for p in PATTERNS:

    p["compiled"] = re.compile(

        p["regex"],

        re.IGNORECASE | re.MULTILINE

    )


# =========================
# SCANNER
# =========================

def scan_files(

    files: List[Dict]

) -> List[Dict]:

    findings = []

    seen = set()


    for file in files:

        path = file["path"]

        code = file["code"]

        lines = code.split("\n")


        for i, line in enumerate(lines):

            for rule in PATTERNS:

                if rule["compiled"].search(line):

                    key = (

                        path,

                        rule["name"],

                        i

                    )

                    if key in seen:

                        continue


                    seen.add(key)


                    findings.append({

                        "file": path,

                        "issue": rule["name"],

                        "severity": rule["severity"],

                        "line": i + 1,

                        "snippet": line.strip()

                    })


    logger.info(

        f"OWASP findings: {len(findings)}"

    )


    return findings