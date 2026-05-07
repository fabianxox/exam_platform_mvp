from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL= 'postgresql://postgres:123@localhost/mvp'
#Purpose: Database location + credentials.

engine = create_engine(DATABASE_URL)
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