from sqlalchemy import Column, Boolean, Integer, String, TIMESTAMP, text, ForeignKey, Enum
from enum import Enum as EnumBase
from app.utils.db import Base


class State(EnumBase):
    QUOTED = "quoted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Conversation(Base):
    __tablename__ = "conversations"

    conversation_id = Column(Integer, primary_key=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    service_provider_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    state = Column(Enum(State), nullable=False, default=State.QUOTED.value)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
