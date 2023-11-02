from fastapi import HTTPException
from starlette import status

from app.repositories.conversation_repository import conversation_repository
from app.schemas.conversation_schema import ConversationGet, ConversationPost, ConversationSchema


def get_conversation_by_id(conversation_id: int) -> ConversationSchema:
    return conversation_repository.get_conversation_by_id(conversation_id)


def get_conversations_from_user_by_id_pag(user_id: int, page: int, size: int) -> list[ConversationGet]:
    return conversation_repository.get_conversations_by_user_id_pag(user_id, page, size)


def create_conversation(conversation: ConversationPost) -> ConversationGet:
    if conversation.customer_id == conversation.service_provider_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Customer and service provider must be different")
    return conversation_repository.create_conversation(conversation)


def delete_conversation(conversation_id: int) -> None:
    return conversation_repository.delete_conversation(conversation_id)
