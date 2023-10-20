from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP, text, ForeignKey

from app.utils.db import Base


class UKLink(Base):
    __tablename__ = "uk_links"

    uk_link_id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    keyword_id = Column(Integer, ForeignKey('keywords.keyword_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
