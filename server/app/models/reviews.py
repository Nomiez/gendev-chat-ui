from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP, text as fun_text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship

from app.utils.db import Base


class MyBase(Base):
    __abstract__ = True

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}


class Review(MyBase):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, nullable=False, index=True)
    personal = Column(Integer, nullable=False)
    working = Column(Integer, nullable=False)
    payment = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    author = relationship("User", back_populates="written_reviews", foreign_keys="Review.author_id")
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    users = relationship("User", back_populates="others_reviews", foreign_keys="Review.user_id")
    likes = relationship("User", secondary="likes", back_populates="likes")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=fun_text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=fun_text('now()'))

    __table_args__ = (
        CheckConstraint('personal between 1 and 10', name='personal_check'),
        CheckConstraint('working between 1 and 10', name='working_check'),
        CheckConstraint('payment between 1 and 10', name='payment_check'),
        {})
