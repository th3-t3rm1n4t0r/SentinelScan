from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env first
load_dotenv()

# =========================
# SETTINGS (Self-contained)
# =========================
class Settings(BaseSettings):
    APP_NAME: str = "SentinelScan API"
    CORS_ORIGINS: str = "*"  # or "http://localhost:3000,https://yourdomain.com"
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

# =========================
# DATABASE (Simple stub - replace with real DB later)
# =========================
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

# SQLite for development (replace with PostgreSQL/MySQL later)
DATABASE_URL = "sqlite:///./sentinelscan.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
Base.metadata.create_all(bind=engine)

# =========================
# LOGGER SETUP
# =========================
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('sentinelscan.log')
        ]
    )

setup_logger()
logger = logging.getLogger("sentinel_scan.main")

# =========================
# FASTAPI APP
# =========================
app = FastAPI(
    title=settings.APP_NAME,
    description="""
AI-powered OWASP vulnerability scanner.

Features:
- GitHub repo scanning
- OWASP Top 10 detection
- AI-powered fix suggestions
- automatic Pull Request creation
- PII masking
- webhook integration
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
    allow_origins=[origin.strip() for origin in settings.CORS_ORIGINS.split(",") if settings.CORS_ORIGINS != "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# TEMPORARY ROUTERS (Create these files next)
# =========================
# Create these placeholder routers to avoid import errors

# api/health.py placeholder
from fastapi import status
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai_service": "ready"
    }

# api/scan.py placeholder (basic version)
@app.post("/scan", tags=["Security Scan"])
async def scan_repo(repo_url: str):
    return {
        "repo_url": repo_url,
        "status": "scan_queued",
        "scan_id": "temp-scan-123"
    }

# =========================
# STARTUP EVENT
# =========================
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing SentinelScan API...")
    logger.info(f"Database: {DATABASE_URL}")
    logger.info("SentinelScan API started successfully!")

# =========================
# SHUTDOWN EVENT
# =========================
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("SentinelScan API shutting down...")

# =========================
# ROOT ENDPOINT
# =========================
@app.get("/", tags=["System"])
async def home():
    return {
        "service": "SentinelScan",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "version": "2.0",
        "ai_model": settings.get("AI_MODEL", "gpt-4o-mini")
    }