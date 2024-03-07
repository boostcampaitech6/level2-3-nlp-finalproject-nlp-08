from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text

class UserFeedback(Base):
    __tablename__ = "userfeedbacks"

    id = Column(Integer,primary_key=True,nullable=False)
    question = Column(String,nullable=False)
    answer = Column(String,nullable=False)
    context = Column(String,nullable=False)
    like = Column(Boolean, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
