from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP, text as fun_text, ForeignKey

from app.utils.db import Base


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, nullable=False, index=True)
    personal = Column(String, nullable=False, unique=True)
    working = Column(String, nullable=False)
    payment = Column(String, nullable=False)
    text = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=fun_text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=fun_text('now()'))
