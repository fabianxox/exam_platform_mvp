from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

import schema
from core.hash import hash_pw
from database.session import get_db
from models.user import User
from core.logger import logger

router = APIRouter(tags=["user"])


@router.post("/user", response_model=schema.userOut, status_code=status.HTTP_201_CREATED)
def create_user(data: schema.userCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == data.email).first()

        if existing_user:
            logger.warning(f"Duplicate signup attempt: {data.email}")
            raise HTTPException(409, "User already exists")

        new_user = User(
            email=data.email,
            password=hash_pw(data.password),
            role="student"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        logger.info(f"User created: {new_user.email}")

        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "User already exists")

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"DB error: {e}", exc_info=True)
        raise HTTPException(500, "Database error")