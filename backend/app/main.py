from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.scan import router as scan_router
from api.health import router as health_router

from app.database import Base, engine
from app.config import settings


# =========================
# LOGGING
# =========================

logging.basicConfig(

    level=settings.LOG_LEVEL,

    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"

)

logger = logging.getLogger(
    "sentinel_scan.main"
)


# =========================
# APP
# =========================

app = FastAPI(

    title=settings.APP_NAME,

    description="AI powered OWASP vulnerability scanner",

    version="2.0",

    docs_url="/docs",

    redoc_url="/redoc"

)


# =========================
# CORS (frontend access)
# =========================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


# =========================
# STARTUP EVENT
# =========================

@app.on_event("startup")

def startup():

    logger.info("Creating database tables")

    Base.metadata.create_all(bind=engine)

    logger.info("SentinelScan API started")


# =========================
# ROUTES
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
# ROOT
# =========================

@app.get("/")

def home():

    return {

        "message": "SentinelScan backend running",

        "docs": "/docs",

        "health": "/health",

        "version": "2.0"

    }    