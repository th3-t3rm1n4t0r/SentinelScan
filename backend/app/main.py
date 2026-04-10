from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import logging

from api.scan import router as scan_router
from api.health import router as health_router

from app.database import Base, engine
from app.config import settings

from app.logger import setup_logger


# =========================
# LOGGER
# =========================

setup_logger()

logger = logging.getLogger(
    "sentinel_scan.main"
)


# =========================
# FASTAPI APP
# =========================

app = FastAPI(

    title=settings.APP_NAME,

    description="""
AI-powered OWASP vulnerability scanner.

Features:

• GitHub repo scanning
• OWASP Top 10 detection
• AI-powered fix suggestions
• automatic Pull Request creation
• PII masking
• webhook integration
""",

    version="2.0",

    docs_url="/docs",

    redoc_url="/redoc",

    openapi_tags=[

        {
            "name": "Security Scan",
            "description": "Repository vulnerability scanning"
        },

        {
            "name": "System",
            "description": "Health & system endpoints"
        }

    ]

)


# =========================
# CORS
# =========================

app.add_middleware(

    CORSMiddleware,

    allow_origins=settings.CORS_ORIGINS or ["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


# =========================
# STARTUP EVENT
# =========================

@app.on_event("startup")
def startup_event():

    logger.info(

        "Initializing database"

    )

    Base.metadata.create_all(

        bind=engine

    )

    logger.info(

        "SentinelScan API started"

    )


# =========================
# SHUTDOWN EVENT
# =========================

@app.on_event("shutdown")
def shutdown_event():

    logger.info(

        "SentinelScan shutting down"

    )


# =========================
# ROUTERS
# =========================

app.include_router(

    scan_router,

    prefix="/scan",

    tags=["Security Scan"]

)


app.include_router(

    health_router,

    prefix="/health",

    tags=["System"]

)


# =========================
# ROOT ENDPOINT
# =========================

@app.get(
    "/",
    tags=["System"]
)

def home():

    return {

        "service": "SentinelScan",

        "status": "running",

        "docs": "/docs",

        "health": "/health",

        "version": "2.0"

    }   