from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP, text, ForeignKey, UniqueConstraint

from app.utils.db import Base


class Like(Base):
    __tablename__ = "likes"

    like_id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    review_id = Column(Integer, ForeignKey('reviews.review_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    __table_args__ = (UniqueConstraint('user_id', 'review_id', name='_user_review_uc'), )
