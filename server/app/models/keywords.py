from __future__ import annotations
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.utils.db import Base


class Keyword(Base):
    __tablename__ = "keywords"

    keyword_id = Column(Integer, primary_key=True, nullable=False, index=True)
    keyword = Column(String, nullable=False, unique=True)
    users = relationship("User", secondary="uk_links", back_populates="keywords")
