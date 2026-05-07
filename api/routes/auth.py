from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import schema
from database.session import get_db
from models.user import User
import core
from core.logger import logger

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=schema.TokenOut)
def login(data: schema.LoginSchema, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == data.email).first()

        if not user or not core.hash.verify_password(data.password, user.password):
            logger.warning(f"Invalid login attempt: {data.email}")
            raise HTTPException(401, "Invalid credentials")

        token = core.hash.create_access_token({
            "user_id": user.id,
            "role": user.role
        })

        logger.info(f"User logged in: {user.email}")

        return {"access_token": token}

    except SQLAlchemyError as e:
        logger.error(f"Login DB error: {e}", exc_info=True)
        raise HTTPException(500, "Database error")