from fastapi import Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

import logging
import secrets

from app.database import SessionLocal
from app.config import settings


logger = logging.getLogger(
    "sentinel_scan.dependencies"
)


# =========================
# DATABASE DEPENDENCY
# =========================

def get_db() -> Session: # type: ignore

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================
# API KEY VALIDATION
# =========================

def verify_api_key(

    x_api_key: str | None = Header(

        default=None,

        alias="x-api-key"

    ),

    authorization: str | None = Header(

        default=None

    )

) -> bool:

    """
    Supports:

    x-api-key header
    Authorization: Bearer TOKEN
    """

    token = None


    # Bearer token support
    if authorization and authorization.startswith(

        "Bearer "

    ):

        token = authorization.replace(

            "Bearer ",

            ""

        )


    # fallback header
    elif x_api_key:

        token = x_api_key


    if not token:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="API key missing"

        )


    valid_keys = {

        settings.WEBHOOK_SECRET

    }


    if not any(

        secrets.compare_digest(

            token,

            k

        )

        for k in valid_keys

        if k

    ):

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Invalid API key"

        )


    return True


# =========================
# GITHUB TOKEN
# =========================

def get_github_token() -> str:

    token = getattr(

        settings,

        "GITHUB_TOKEN",

        None

    )


    if not token:

        logger.error(

            "GITHUB_TOKEN missing"

        )


        raise HTTPException(

            status_code=500,

            detail="GitHub token not configured"

        )


    return token


# =========================
# OPENAI KEY
# =========================

def get_openai_key() -> str:

    key = getattr(

        settings,

        "OPENAI_API_KEY",

        None

    )


    if not key:

        logger.error(

            "OPENAI_API_KEY missing"

        )


        raise HTTPException(

            status_code=500,

            detail="OpenAI key not configured"

        )


    return key


# =========================
# OPTIONAL ADMIN CHECK
# =========================

def verify_admin_key(

    x_admin_key: str | None = Header(

        default=None,

        alias="x-admin-key"

    )

):

    admin_key = getattr(

        settings,

        "ADMIN_SECRET",

        None

    )


    if not admin_key:

        raise HTTPException(

            status_code=500,

            detail="Admin key not configured"

        )


    if not x_admin_key:

        raise HTTPException(

            status_code=401,

            detail="Admin key required"

        )


    if not secrets.compare_digest(

        x_admin_key,

        admin_key

    ):

        raise HTTPException(

            status_code=403,

            detail="Invalid admin key"

        )


    return True 