from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True)
    user_id = Column(
      Integer,
      ForeignKey("users.id"),
      nullable=False
    )

    exam_id = Column(
      Integer,
      ForeignKey("exams.id"),
      nullable=False
    )

    score = Column(Integer, default=0)
    completed = Column(Boolean, default=False)

    # 🔗 relationships
    user = relationship("User", back_populates="attempts")
    exam = relationship("Exam", back_populates="attempts")
    answers = relationship("Answer", back_populates="attempt")