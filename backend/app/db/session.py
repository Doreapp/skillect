"""Database session"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import SETTINGS

engine = create_engine(SETTINGS.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
