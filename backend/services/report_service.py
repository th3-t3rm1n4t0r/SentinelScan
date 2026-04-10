import json
import os
import uuid
import logging

from datetime import datetime

from typing import List, Dict, Optional


logger = logging.getLogger(
    "sentinel_scan.report"
)


# =========================
# CONFIG
# =========================

REPORT_DIR = os.getenv(
    "REPORT_DIR",
    "reports"
)

os.makedirs(
    REPORT_DIR,
    exist_ok=True
)


# =========================
# CREATE REPORT
# =========================

def create_report(

    findings: List[Dict],

    fixes: Optional[List[Dict]] = None,

    repo: Optional[str] = None,

    branch: Optional[str] = None

) -> Dict:


    report_id = str(
        uuid.uuid4()
    )[:8]


    timestamp = datetime.utcnow().isoformat()


    json_path = os.path.join(

        REPORT_DIR,

        f"scan_{report_id}.json"

    )


    html_path = os.path.join(

        REPORT_DIR,

        f"scan_{report_id}.html"

    )


    findings = deduplicate_findings(

        findings
    )


    severity_count = {

        "critical": 0,

        "high": 0,

        "medium": 0,

        "low": 0

    }


    for f in findings:

        sev = str(

            f.get(

                "severity",

                "low"

            )

        ).lower()


        severity_count.setdefault(

            sev,

            0

        )


        severity_count[sev] += 1


    report_data = {

        "report_id": report_id,

        "repo": repo,

        "branch": branch,

        "generated_at": timestamp,

        "summary": {

            "total_issues": len(findings),

            "severity": severity_count

        },

        "findings": findings,

        "fixes": fixes or []

    }


    # =====================
    # SAVE JSON
    # =====================

    with open(

        json_path,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            report_data,

            f,

            indent=2

        )


    # =====================
    # SAVE HTML
    # =====================

    html_content = build_html_report(

        report_data

    )


    with open(

        html_path,

        "w",

        encoding="utf-8"

    ) as f:


        f.write(

            html_content

        )


    logger.info(

        f"report created {report_id}"

    )


    return {

        "report_id": report_id,

        "json_path": json_path,

        "html_path": html_path,

        "summary": report_data["summary"]

    }


# =========================
# HTML REPORT
# =========================

def build_html_report(

    data: Dict

) -> str:


    rows = ""


    for f in data["findings"]:


        severity = str(

            f.get(

                "severity",

                "low"

            )

        ).lower()


        rows += f"""

<tr>

<td>{escape_html(f.get("file"))}</td>

<td>{escape_html(f.get("issue"))}</td>

<td class="badge {severity}">{severity}</td>

<td>{f.get("line")}</td>

<td>

<code>

{escape_html(f.get("snippet",""))}

</code>

</td>

</tr>

"""


    fixes_html = ""


    for fix in data.get(

        "fixes",

        []

    ):


        fixes_html += f"""

<div class="fix">

<b>{escape_html(fix.get("issue"))}</b>

<pre>

{escape_html(fix.get("fix",""))}

</pre>

<small>

{escape_html(fix.get("explanation",""))}

</small>

</div>

"""


    html = f"""

<html>

<head>

<title>SentinelScan Report</title>

<style>

body {{

font-family: Arial;

margin: 40px;

background:#f4f6f8;

}}

h1 {{

color:#222;

}}

table {{

border-collapse: collapse;

width:100%;

background:white;

}}

th,td {{

border:1px solid #ddd;

padding:8px;

}}

th {{

background:#111;

color:white;

}}

.badge {{

padding:4px 8px;

border-radius:4px;

font-size:12px;

}}

.critical {{

background:#ff4d4f;

color:white;

}}

.high {{

background:#fa8c16;

color:white;

}}

.medium {{

background:#1677ff;

color:white;

}}

.low {{

background:#888;

color:white;

}}

.fix {{

background:white;

padding:12px;

margin:10px 0;

border-left:4px solid #28a745;

}}

.summary-box {{

background:white;

padding:15px;

margin-bottom:20px;

border-radius:6px;

}}

</style>

</head>

<body>

<h1>SentinelScan Security Report</h1>

<div class="summary-box">

<p><b>Repository:</b> {escape_html(data.get("repo"))}</p>

<p><b>Branch:</b> {escape_html(data.get("branch"))}</p>

<p><b>Generated:</b> {data.get("generated_at")}</p>

<p><b>Total Issues:</b> {data["summary"]["total_issues"]}</p>

</div>


<h2>Severity Summary</h2>

<ul>

<li>Critical: {data["summary"]["severity"]["critical"]}</li>

<li>High: {data["summary"]["severity"]["high"]}</li>

<li>Medium: {data["summary"]["severity"]["medium"]}</li>

<li>Low: {data["summary"]["severity"]["low"]}</li>

</ul>


<h2>Findings</h2>

<table>

<tr>

<th>File</th>

<th>Issue</th>

<th>Severity</th>

<th>Line</th>

<th>Code</th>

</tr>

{rows}

</table>


<h2>AI Fix Suggestions</h2>

{fixes_html}


</body>

</html>

"""


    return html


# =========================
# HELPERS
# =========================

def deduplicate_findings(

    findings: List[Dict]

):

    seen = set()

    result = []


    for f in findings:

        key = (

            f.get("file"),

            f.get("issue"),

            f.get("line")

        )


        if key in seen:

            continue


        seen.add(key)

        result.append(f)


    return result


def escape_html(

    text: str

) -> str:


    if not text:

        return ""


    return (

        str(text)

        .replace("&", "&amp;")

        .replace("<", "&lt;")

        .replace(">", "&gt;")

    )