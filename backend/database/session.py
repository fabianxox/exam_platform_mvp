from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
engine = create_engine(settings.DATABASE_URL)
#Meaning: Prepare connection to database.
#Note: Does NOT connect yet.

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#dependency
def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()