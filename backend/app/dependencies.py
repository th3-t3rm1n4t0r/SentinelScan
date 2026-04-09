from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
import logging

from app.database import SessionLocal
from app.config import settings


logger = logging.getLogger(
    "sentinel_scan.dependencies"
)


# =========================
# DATABASE DEPENDENCY
# =========================

def get_db():

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

):

    """
    supports:

    x-api-key header
    Authorization: Bearer TOKEN
    """

    token = None


    # Bearer token support
    if authorization and authorization.startswith("Bearer "):

        token = authorization.replace(
            "Bearer ",
            ""
        )


    # fallback to x-api-key
    elif x_api_key:

        token = x_api_key


    if not token:

        raise HTTPException(

            status_code=401,

            detail="API key missing"
        )


    if token != settings.WEBHOOK_SECRET:

        raise HTTPException(

            status_code=403,

            detail="Invalid API key"
        )


    return True


# =========================
# GITHUB TOKEN
# =========================

def get_github_token():

    if not settings.GITHUB_TOKEN:

        logger.error(
            "GITHUB_TOKEN missing"
        )

        raise HTTPException(

            status_code=500,

            detail="GitHub token not configured"
        )


    return settings.GITHUB_TOKEN


# =========================
# OPENAI KEY
# =========================

def get_openai_key():

    if not settings.OPENAI_API_KEY:

        logger.error(
            "OPENAI_API_KEY missing"
        )

        raise HTTPException(

            status_code=500,

            detail="OpenAI key not configured"
        )


    return settings.OPENAI_API_KEY 
    