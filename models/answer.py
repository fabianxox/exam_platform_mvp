from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database.base import Base


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)

    attempt_id = Column(Integer, ForeignKey("attempts.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))

    selected_answer = Column(String)
    is_correct = Column(Boolean)

    # relationships
    attempt = relationship("Attempt", back_populates="answers")
    question = relationship("Question")