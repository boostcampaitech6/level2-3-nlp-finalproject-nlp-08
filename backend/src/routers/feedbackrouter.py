from typing import Annotated

from fastapi import APIRouter, Depends
from database import get_db
from sqlalchemy.orm import Session

from schemas import UserFeedbackBase
import models

feedbackrouter = APIRouter()

@feedbackrouter.post('/feedback/')
async def create_userfeedback(feedback: UserFeedbackBase, db: Annotated[Session, Depends(get_db)]):
    db_feedback = models.UserFeedback(question=feedback.question, 
                                      answer=feedback.answer, 
                                      context=feedback.context,
                                      like=feedback.like)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)

    return db_feedback

@feedbackrouter.get('/feedback/')
async def get_userfeedback(db: Annotated[Session, Depends(get_db)]):
    all_feedbacks = db.query(models.UserFeedback).all()

    return all_feedbacks


