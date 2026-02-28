from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from enigma_app.config import DATABASE_URL, SQLALCHEMY_ENGINE_OPTIONS

engine = create_engine(DATABASE_URL, **SQLALCHEMY_ENGINE_OPTIONS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency для FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()