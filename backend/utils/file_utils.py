import os
import uuid
import logging

from typing import Optional


logger = logging.getLogger(
    "sentinel_scan.file_utils"
)


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

    if not filename:

        return False


    filename = filename.lower()


    return any(

        filename.endswith(ext)

        for ext in SUPPORTED_EXTENSIONS

    )


# =========================
# SAFE FILE READ
# =========================

def safe_read_file(

    path: str,

    max_size: int = 200_000

) -> Optional[str]:


    try:

        if not path:

            return None


        path = os.path.abspath(path)


        if not os.path.exists(path):

            logger.warning(
                f"file not found {path}"
            )

            return None


        size = os.path.getsize(path)


        if size > max_size:

            logger.warning(
                f"file too large {path}"
            )

            return None


        with open(

            path,

            "r",

            encoding="utf-8",

            errors="ignore"

        ) as f:

            content = f.read()


        # skip binary-like files
        if is_binary(content):

            return None


        return content


    except Exception as e:

        logger.warning(
            f"read failed {path} {str(e)}"
        )

        return None


# =========================
# SAFE DIRECTORY CREATE
# =========================

def ensure_dir(

    path: str

):

    if not path:

        return


    try:

        os.makedirs(

            path,

            exist_ok=True

        )

    except Exception as e:

        logger.error(
            f"dir create failed {path} {str(e)}"
        )


# =========================
# UNIQUE FILE NAME
# =========================

def unique_filename(

    prefix: str,

    extension: str

) -> str:


    prefix = sanitize_filename(

        prefix

    )


    extension = extension.lower().replace(

        ".",

        ""

    )


    uid = str(

        uuid.uuid4()

    )[:8]


    return f"{prefix}_{uid}.{extension}"


# =========================
# HELPERS
# =========================

def sanitize_filename(

    name: str

) -> str:


    if not name:

        return "file"


    return "".join(

        c for c in name

        if c.isalnum() or c in ("_", "-")

    )[:60]


def is_binary(

    text: str

) -> bool:


    if not text:

        return False


    non_printable = sum(

        1 for c in text

        if ord(c) < 9 or (13 < ord(c) < 32)

    )


    return non_printable > 20  
