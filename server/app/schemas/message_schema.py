import inspect
from datetime import datetime
from typing import Optional, Type, Annotated

from fastapi import Form
from pydantic import BaseModel, BeforeValidator
from pydantic.fields import Field
from enum import Enum

from app.models.conversation_messages import MessageType, SenderType


class ConversationMessage(BaseModel):
    message_id: int
    message_type: MessageType
    message_attachment: Optional[str]
    text: str
    sender_type: SenderType
    service_provider_reaction: Optional[str]
    customer_reaction: Optional[str]
    created_at: datetime
    received_at: Optional[datetime]
    read_at: Optional[datetime]
    updated_at: datetime
    deleted_at: Optional[datetime]
    hidden_at: Optional[datetime]
    conversation_id: int


class ConversationMessagePut(BaseModel):
    message_type: Optional[MessageType]
    message_attachment: Optional[str]
    text: Optional[str]
    sender_type: Optional[SenderType]
    service_provider_reaction: Optional[str]
    customer_reaction: Optional[str]
    received_at: Optional[datetime]
    read_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    hidden_at: Optional[datetime]


class ConversationMessagePost(BaseModel):
    text: str
    hidden_at: Optional[datetime]


class ConversationMessagePostInternal(BaseModel):
    text: str
    hidden_at: Optional[datetime] = None
    conversation_id: Optional[int] = None
    message_type: Optional[MessageType] = None
    message_attachment: Optional[str] = None
    sender_type: Optional[SenderType] = None


class ReadingState(Enum):
    RECEIVED = "received"
    READ = "read"
