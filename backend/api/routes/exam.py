from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import schema
from database.session import get_db
from models.user import User
import core
from core.logger import logger

import models
from api import dev
from models.question import Question
from models.attempt import Attempt

from datetime import datetime, timedelta

from fastapi import Query

router = APIRouter(tags=["exam"])

@router.post("/exam/{exam_id}/start")
def start_exam(
    exam_id: int,
    user=Depends(dev.student_only),
    db: Session = Depends(get_db)
):

    # check existing active attempt
    existing_attempt = db.query(Attempt).filter(
        Attempt.user_id == user.id,
        Attempt.exam_id == exam_id,
        Attempt.completed == False
    ).first()

    # reuse existing attempt
    if existing_attempt:

        logger.info(
            f"Existing attempt reused | "
            f"user={user.id} exam={exam_id}"
        )

        return existing_attempt

    # create fresh attempt
    attempt = Attempt(
        user_id=user.id,
        exam_id=exam_id
    )

    db.add(attempt)

    db.commit()

    db.refresh(attempt)

    logger.info(
        f"New attempt created | "
        f"user={user.id} exam={exam_id}"
    )

    return attempt

@router.post("/exam/{exam_id}/submit")
def submit_exam(
    exam_id: int,
    data: schema.SubmitExam,
    user=Depends(dev.student_only),
    db: Session = Depends(get_db)
):

    # find active attempt
    attempt = db.query(Attempt).filter(
        Attempt.user_id == user.id,
        Attempt.exam_id == exam_id,
        Attempt.completed == False
    ).first()

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Active attempt not found"
        )

    # fetch exam
    exam = db.query(models.exam.Exam).filter(
        models.exam.Exam.id == exam_id
    ).first()

    if not exam:
        raise HTTPException(
            status_code=404,
            detail="Exam not found"
        )

    # timer validation
    exam_end_time = (
        attempt.created_at +
        timedelta(minutes=exam.duration)
    )

    if datetime.utcnow() > exam_end_time:

        logger.warning(
            f"Exam submission rejected due to timeout | "
            f"user={user.id} exam={exam_id}"
        )

        raise HTTPException(
            status_code=400,
            detail="Exam time expired"
        )

    score = 0

    # valid question ids for this exam
    links = db.query(models.exam_question.ExamQuestion).filter(
        models.exam_question.ExamQuestion.exam_id == exam_id
    ).all()

    valid_question_ids = {
        l.question_id for l in links
    }

    for ans in data.answers:

        # prevent invalid question submission
        if ans.question_id not in valid_question_ids:
            continue

        question = db.query(Question).filter(
            Question.id == ans.question_id
        ).first()

        if not question:
            continue

        is_correct = (
            question.correct_answer == ans.answer
        )

        if is_correct:
            score += 1

        # store answer
        answer_row = models.answer.Answer(
            attempt_id=attempt.id,
            question_id=question.id,
            selected_answer=ans.answer,
            is_correct=is_correct
        )

        db.add(answer_row)

    # finalize attempt
    attempt.score = score

    attempt.completed = True

    attempt.submitted_at = datetime.utcnow()

    db.commit()

    logger.info(
        f"Exam submitted | "
        f"user={user.id} exam={exam_id} score={score}"
    )

    return {
        "score": score
    }

@router.get("/exam/{exam_id}/result")
def get_result(exam_id: int, user=Depends(dev.student_only), db: Session = Depends(get_db)):

    attempt = db.query(Attempt).filter(
        Attempt.user_id == user.id,
        Attempt.exam_id == exam_id
    ).first()

    return {"score": attempt.score}

@router.get("/exam/{exam_id}", response_model=schema.ExamOut)
def get_exam(
    exam_id: int,
    user=Depends(dev.get_current_user),
    db: Session = Depends(get_db)
):

    exam = db.query(models.exam.Exam).filter(
        models.exam.Exam.id == exam_id
    ).first()

    if not exam:
        raise HTTPException(404, "Exam not found")

    # get linked question ids
    links = db.query(models.exam_question.ExamQuestion).filter(
        models.exam_question.ExamQuestion.exam_id == exam_id
    ).all()

    question_ids = [l.question_id for l in links]

    # fetch questions
    questions = db.query(Question).filter(
        Question.id.in_(question_ids)
    ).all()

    # dynamically attach
    exam.questions = questions

    return exam

@router.get("/exams")
def get_exams(

    user=Depends(dev.student_only),

    page: int = Query(
        default=1,
        ge=1
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),

    db: Session = Depends(get_db)
):

    try:

        # calculate offset
        offset = (page - 1) * limit

        exams = db.query(models.exam.Exam)\
            .offset(offset)\
            .limit(limit)\
            .all()

        return {
            "page": page,
            "limit": limit,
            "count": len(exams),
            "items": exams
        }

    except SQLAlchemyError as e:

        logger.error(
            f"Error fetching exams: {e}",
            exc_info=True
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )