from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP, text, ForeignKey

from app.utils.db import Base


class Keyword(Base):
    __tablename__ = "keywords"

    keyword_id = Column(Integer, primary_key=True, nullable=False, index=True)
    keyword = Column(String, nullable=False, unique=True)

