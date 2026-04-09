from fastapi import FastAPI
from api.scan import router as scan_router
from api.health import router as health_router

from app.database import Base, engine

# create database tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(

    title="SentinelScan API",

    description="AI powered OWASP vulnerability scanner",

    version="2.0"

)

# routes
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


@app.get("/")

def home():

    return {

        "message": "SentinelScan backend running",

        "docs": "/docs",

        "health": "/health"

    }