from datetime import datetime

from pydantic import BaseModel

from app.models.conversations import State


# TODO: Add last new message + count of unread messages
class ConversationGet(BaseModel):
    conversation_id: int
    customer_id: int
    service_provider_id: int
    state: State

class ConversationSchema(BaseModel):
    conversation_id: int
    customer_id: int
    service_provider_id: int
    state: State
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None



class ConversationPost(BaseModel):
    customer_id: int
    service_provider_id: int
