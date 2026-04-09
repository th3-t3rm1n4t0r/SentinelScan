
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

import logging

from app.config import settings


logger = logging.getLogger(
    "sentinel_scan.database"
)


# =========================
# DATABASE ENGINE
# =========================

engine = create_engine(

    settings.DATABASE_URL,

    # connection pool
    poolclass=QueuePool,

    pool_size=10,          # persistent connections
    max_overflow=20,       # burst connections
    pool_timeout=30,       # seconds to wait for connection
    pool_recycle=1800,     # refresh connection every 30 min

    # reliability
    pool_pre_ping=True,

    # debugging
    echo=settings.DEBUG,

    # SQLAlchemy 2.x behaviour
    future=True

)


logger.info(
    "Database engine initialized"
)


# =========================
# SESSION FACTORY
# =========================

SessionLocal = sessionmaker(

    bind=engine,

    autocommit=False,

    autoflush=False,

    expire_on_commit=False

)


# =========================
# BASE MODEL
# =========================

Base = declarative_base()


# =========================
# DB DEPENDENCY (FastAPI)
# =========================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================
# CREATE TABLES
# =========================

def create_tables():

    """
    Create tables without Alembic.
    Recommended only for development.
    """

    logger.info(
        "Creating database tables"
    )

    Base.metadata.create_all(

        bind=engine

    )


# =========================
# HEALTH CHECK
# =========================

def check_db_connection() -> bool:

    try:

        with engine.connect() as conn:

            conn.execute("SELECT 1")

        return True

    except Exception as e:

        logger.error(

            f"DB connection failed {str(e)}"

        )

        return False   
