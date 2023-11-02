from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP, text, ForeignKey, Enum
from enum import Enum as EnumBase

from sqlalchemy.orm import relationship

from app.utils.db import Base


class State(EnumBase):
    QUOTED = "quoted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class MyBase(Base):
    __abstract__ = True

    def to_dict(self):
        return {field.name: getattr(self, field.name) for field in self.__table__.c}


class Conversation(MyBase):
    __tablename__ = "conversations"

    conversation_id = Column(Integer, primary_key=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    customer = relationship("User", back_populates="conversations_as_customer", foreign_keys="Conversation.customer_id")
    service_provider_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    service_provider = relationship("User", back_populates="conversations_as_service_provider",
                                    foreign_keys="Conversation.service_provider_id")
    state = Column(Enum(State), nullable=False, default=State.QUOTED)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
