from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models.conversations import State
from app.schemas.message_schema import ConversationMessage
from app.schemas.user_schema import UserInReview


class ConversationGet(BaseModel):
    conversation_id: int
    customer_id: int
    service_provider_id: int
    state: State
    last_message: Optional[ConversationMessage]
    customer: UserInReview
    service_provider: UserInReview
    unread_messages: int


class ConversationSchema(BaseModel):
    conversation_id: int
    customer_id: int
    service_provider_id: int
    state: State
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    customer: UserInReview
    service_provider: UserInReview


class ConversationPost(BaseModel):
    customer_id: int
    service_provider_id: int
