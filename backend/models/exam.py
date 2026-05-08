from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.base import Base
from sqlalchemy import DateTime
from datetime import datetime

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    duration = Column(Integer)
    created_at = Column(
      DateTime,
      default=datetime.utcnow
    )
    # 🔗 relationships
    attempts = relationship("Attempt", back_populates="exam")
    exam_questions = relationship("ExamQuestion", back_populates="exam")