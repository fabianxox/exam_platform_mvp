from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base
from sqlalchemy import DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="student", nullable=False)

    # 🔗 relationship
    attempts = relationship("Attempt", back_populates="user")