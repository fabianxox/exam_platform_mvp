from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.dev import admin_only
from database.session import get_db
from models.exam import Exam
from models.question import Question
from models.exam_question import ExamQuestion
from schema import ExamCreate, ExamCreateOut
from core.logger import logger

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/exam", response_model=ExamCreateOut)
def create_exam(
    data: ExamCreate,
    db: Session = Depends(get_db),
    user = Depends(admin_only)
):
    try:
        exam = Exam(
            title=data.title,
            duration=data.duration
        )

        db.add(exam)
        db.commit()
        db.refresh(exam)

        logger.info(f"Admin {user.email} created exam: {exam.title}")

        return exam

    except Exception as e:
        db.rollback()
        logger.error(f"Exam creation failed: {e}", exc_info=True)
        raise HTTPException(500, "Failed to create exam")

from models.question import Question
import schema
@router.post("/question")
def add_question(data: schema.QuestionCreate, user=Depends(admin_only), db: Session = Depends(get_db)):
    q = Question(
        text=data.text,
        option_a=data.option_a,
        option_b=data.option_b,
        option_c=data.option_c,
        option_d=data.option_d,
        correct_answer=data.correct_answer
    )
    db.add(q)
    db.commit()
    db.refresh(q)
    return q

@router.post("/exam/{exam_id}/add-question/{question_id}")
def link_question(exam_id: int, question_id: int, user=Depends(admin_only), db: Session = Depends(get_db)):

    link = ExamQuestion(
        exam_id=exam_id,
        question_id=question_id
    )

    db.add(link)
    db.commit()

    return {"msg": "linked"}