from sqlalchemy import Column, Integer, String, TIMESTAMP, text
from sqlalchemy.orm import relationship

from app.utils.db import Base
from app.models.uk_links import UKLink


class MyBase(Base):
    __abstract__ = True

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}


class User(MyBase):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    info_text = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    keywords = relationship("Keyword", secondary="uk_links", back_populates="users")
    likes = relationship("Review", secondary="likes", back_populates="likes")
    written_reviews = relationship("Review", back_populates="users", foreign_keys="Review.author_id")
    others_reviews = relationship("Review", back_populates="users", foreign_keys="Review.user_id")
    conversations_as_customer = relationship("Conversation", back_populates="customer",
                                             foreign_keys="Conversation.customer_id")
    conversations_as_service_provider = relationship("Conversation", back_populates="service_provider",
                                                     foreign_keys="Conversation.service_provider_id")
