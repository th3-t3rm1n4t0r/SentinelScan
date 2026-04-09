import os
from typing import List


# =========================
# EXTENSION FILTER
# =========================

SUPPORTED_EXTENSIONS = (

    ".py",
    ".js",
    ".ts",
    ".java",
    ".go",
    ".rb",
    ".php",
    ".json",
    ".yaml",
    ".yml",
    ".env",
    ".ini",
    ".cfg"

)


def is_supported_file(

    filename: str

) -> bool:

    return filename.endswith(

        SUPPORTED_EXTENSIONS

    )


# =========================
# SAFE FILE READ
# =========================

def safe_read_file(

    path: str,

    max_size: int = 200_000

):

    try:

        if not os.path.exists(path):

            return None


        if os.path.getsize(path) > max_size:

            return None


        with open(

            path,

            "r",

            encoding="utf-8",

            errors="ignore"

        ) as f:

            return f.read()


    except Exception:

        return None


# =========================
# SAFE DIRECTORY CREATE
# =========================

def ensure_dir(

    path: str

):

    os.makedirs(

        path,

        exist_ok=True

    )


# =========================
# UNIQUE FILE NAME
# =========================

def unique_filename(

    prefix: str,

    extension: str

):

    import uuid

    uid = str(uuid.uuid4())[:8]

    return f"{prefix}_{uid}.{extension}"