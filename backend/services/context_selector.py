import logging
import re
from typing import List, Dict

from app.config import settings


logger = logging.getLogger("sentinel_scan.context")


# =========================
# SETTINGS
# =========================

MAX_FILES = settings.MAX_FILES
MAX_CHARS = settings.AI_MAX_CHARS

SUPPORTED_EXTENSIONS = (
    ".py",
    ".js",
    ".ts",
    ".java",
    ".go",
    ".rs",
    ".php",
    ".cs",
    ".cpp",
    ".c",
    ".jsx",
    ".tsx",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".env"
)

# priority keywords
SECURITY_KEYWORDS = (
    "auth",
    "login",
    "password",
    "secret",
    "token",
    "key",
    "crypto",
    "jwt",
    "session",
    "admin",
    "permission",
    "config",
    "database",
    "connection",
    "oauth",
    "env",
)

IGNORE_FOLDERS = (
    "node_modules",
    "dist",
    "build",
    "venv",
    ".git",
    "__pycache__",
    ".next",
    ".cache"
)


# =========================
# MAIN FUNCTION
# =========================

def select_context(files: List[Dict]) -> List[Dict]:

    if not files:
        return []

    logger.info(f"Selecting context from {len(files)} files")

    filtered = filter_files(files)

    prioritized = prioritize_files(filtered)

    trimmed = trim_content(prioritized)

    logger.info(f"Context selected: {len(trimmed)} files")

    return trimmed


# =========================
# FILTER FILES
# =========================

def filter_files(files: List[Dict]) -> List[Dict]:

    result = []

    seen_paths = set()

    for f in files:

        path = f.get("path", "").lower()

        content = f.get("content", "")

        if not path or not content:
            continue

        # skip duplicates
        if path in seen_paths:
            continue

        seen_paths.add(path)

        # extension filter
        if not path.endswith(SUPPORTED_EXTENSIONS):
            continue

        # ignore folders
        if any(folder in path for folder in IGNORE_FOLDERS):
            continue

        # skip binary-like files
        if is_binary(content):
            continue

        result.append(f)

        if len(result) >= MAX_FILES * 2:
            break

    return result


# =========================
# PRIORITIZATION
# =========================

def prioritize_files(files: List[Dict]) -> List[Dict]:

    scored = []

    for f in files:

        path = f.get("path", "").lower()

        content = f.get("content", "").lower()

        score = 0

        # boost security relevant files
        for keyword in SECURITY_KEYWORDS:

            if keyword in path:
                score += 3

            if keyword in content:
                score += 1

        # boost config files
        if "config" in path:
            score += 2

        # boost env
        if ".env" in path:
            score += 4

        # smaller files often more important
        length = len(content)

        if length < 2000:
            score += 1

        scored.append((score, f))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [f for _, f in scored[:MAX_FILES]]


# =========================
# CONTENT TRIMMING
# =========================

def trim_content(files: List[Dict]) -> List[Dict]:

    result = []

    total_chars = 0

    for f in files:

        content = clean_content(f["content"])

        size = len(content)

        if total_chars + size > MAX_CHARS:

            remaining = MAX_CHARS - total_chars

            if remaining <= 0:
                break

            content = content[:remaining]

        result.append({

            "path": f["path"],

            "content": content

        })

        total_chars += len(content)

    return result


# =========================
# HELPERS
# =========================

def is_binary(text: str) -> bool:

    if not text:
        return True

    # detect many non printable chars
    non_printable = sum(

        1 for c in text

        if ord(c) < 9 or (13 < ord(c) < 32)

    )

    return non_printable > 20


def clean_content(text: str) -> str:

    # remove very long base64 strings
    text = re.sub(

        r"[A-Za-z0-9+/]{200,}={0,2}",

        "[BASE64_REMOVED]",

        text

    )

    # remove very long lines
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:

        if len(line) > 800:

            cleaned_lines.append(line[:800])

        else:

            cleaned_lines.append(line)

    return "\n".join(cleaned_lines) 