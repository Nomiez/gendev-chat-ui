from enum import Enum as EnumBase

from sqlalchemy.orm import relationship

from app.utils.db import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text as fun_text, ForeignKey, Enum


class MessageType(EnumBase):
    QUOTE_OFFER = "quote_offer"
    REJECT_QUOTE_MESSAGE = "reject_quote_message"
    ACCEPT_QUOTE_MESSAGE = "accept_quote_message"
    STANDARD_MESSAGE = "standard_message"


class SenderType(EnumBase):
    SERVICE_PROVIDER = "service_provider"
    CUSTOMER = "customer"


class ThreadMessage(Base):
    __tablename__ = "thread_messages"

    message_id = Column(Integer, primary_key=True, nullable=False, index=True)
    message_type = Column(Enum(MessageType), nullable=False)
    message_attachment = Column(String, nullable=True)
    text = Column(String, nullable=False)
    sender_type = Column(Enum(SenderType), nullable=False)
    service_provider_reaction = Column(String, nullable=True)
    customer_reaction = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=fun_text('now()'))
    received_at = Column(TIMESTAMP(timezone=True), nullable=True)
    read_at = Column(TIMESTAMP(timezone=True), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=fun_text('now()'))
    deleted_at = Column(TIMESTAMP(timezone=True), nullable=True)
    hidden_at = Column(TIMESTAMP(timezone=True), nullable=True)
    parent_id = Column(Integer, ForeignKey('conversation_messages.message_id', ondelete='CASCADE'), nullable=False)
    parent = relationship("ConversationMessage",
                          back_populates="children",
                          foreign_keys="ThreadMessage.parent_id")
