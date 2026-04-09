from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

from app.config import settings


# =========================
# DATABASE ENGINE
# =========================

engine = create_engine(

    settings.DATABASE_URL,

    # connection pool
    poolclass=QueuePool,

    pool_size=10,          # persistent connections
    max_overflow=20,       # temporary extra connections
    pool_timeout=30,       # wait time for connection
    pool_recycle=1800,     # recycle connections every 30 min

    # reliability
    pool_pre_ping=True,    # check connection before use

    # debugging
    echo=settings.DEBUG,

    # postgres performance
    future=True
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
# HELPER (optional)
# =========================

def create_tables():

    """
    call once on startup if not using alembic
    """

    Base.metadata.create_all(bind=engine)   