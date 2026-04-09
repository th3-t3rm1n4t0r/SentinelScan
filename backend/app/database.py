from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


# create SQLAlchemy engine
engine = create_engine(

    settings.DATABASE_URL,

    pool_pre_ping=True,      # checks connection before use

    pool_size=10,            # number of connections kept ready

    max_overflow=20,         # extra connections allowed

    echo=settings.DEBUG      # logs SQL queries when DEBUG=True

)


# session factory
SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)


# base model class
Base = declarative_base()



# dependency for FastAPI routes
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()