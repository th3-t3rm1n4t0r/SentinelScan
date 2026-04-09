from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.config import settings


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

    x_api_key: str = Header(None)

):

    if not x_api_key:

        raise HTTPException(

            status_code=401,

            detail="API key missing"

        )

    if x_api_key != settings.WEBHOOK_SECRET:

        raise HTTPException(

            status_code=403,

            detail="Invalid API key"

        )

    return True



# =========================
# GITHUB TOKEN CHECK
# =========================

def get_github_token():

    if not settings.GITHUB_TOKEN:

        raise HTTPException(

            status_code=500,

            detail="GitHub token not configured"

        )

    return settings.GITHUB_TOKEN



# =========================
# OPENAI KEY CHECK
# =========================

def get_openai_key():

    if not settings.OPENAI_API_KEY:

        raise HTTPException(

            status_code=500,

            detail="OpenAI key not configured"

        )

    return settings.OPENAI_API_KEY