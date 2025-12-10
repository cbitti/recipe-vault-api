from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the Engine
engine = create_engine(settings.DATABASE_URL)

# Create the Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for FastAPI Endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()