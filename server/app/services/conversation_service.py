from typing import Optional

from fastapi import HTTPException
from starlette import status

from app.repositories.conversation_repository import conversation_repository
from app.schemas.conversation_schema import ConversationGet, ConversationPost, ConversationSchema
from app.schemas.message_schema import ReadingState
from app.services.conversation_message_service import update_sending_status_by_conversation_id
from app.utils.message_stream import MessageStream
from app.utils.stream_handles import stream_handles as handles


def _update_conversation_reading_state(conversation: ConversationSchema, user_id: int) -> None:
    # Update read state of the messages to received
    if conversation.customer_id == user_id:
        update_sending_status_by_conversation_id(conversation.conversation_id,
                                                 user_id,
                                                 conversation.customer_id,
                                                 ReadingState.RECEIVED)
    elif conversation.service_provider_id == user_id:
        update_sending_status_by_conversation_id(conversation.conversation_id,
                                                 user_id,
                                                 conversation.service_provider_id,
                                                 ReadingState.RECEIVED)


def get_conversation_by_id(conversation_id: int, user_id: Optional[int] = None,
                           censored: bool = False) -> ConversationSchema:
    current_conv = conversation_repository.get_conversation_by_id(conversation_id)
    _update_conversation_reading_state(current_conv, user_id)
    if censored:
        el = MessageStream([current_conv.last_message]) \
            .filter(lambda msg: msg is not None) \
            .filter(MessageStream.hidden_filter(current_conv, user_id)) \
            .map(MessageStream.censor_func(current_conv)) \
            .to_list()
        current_conv.last_message = el[0] if el else None
    return current_conv


def get_conversations_from_user_by_id_pag(user_id: int, page: int, size: int, censored: bool = False) -> list[
    ConversationGet]:
    conversation_list = conversation_repository.get_conversations_by_user_id_pag(user_id, page, size)
    for current_conv in conversation_list:
        _update_conversation_reading_state(current_conv, user_id)
    result = []
    if censored:
        for current_conv in conversation_list:
            el = MessageStream([current_conv.last_message]) \
                .filter(lambda msg: msg is not None) \
                .filter(MessageStream.hidden_filter(current_conv, user_id)) \
                .map(MessageStream.censor_func(current_conv)) \
                .to_list()
            current_conv.last_message = el[0] if el else None
            result.append(current_conv)

        return result
    return conversation_list


def create_conversation(conversation: ConversationPost, user_id: int) -> ConversationGet:
    if conversation.customer_id == conversation.service_provider_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Customer and service provider must be different")
    conversation = conversation_repository.create_conversation(conversation, user_id)
    dict_message = {
        "conversation_id": conversation.conversation_id
    }
    handles.enqueue_message_opt([user_id, (conversation.customer_id
                                           if conversation.customer_id is not user_id
                                           else conversation.service_provider_id)], str(dict_message))
    return conversation


def delete_conversation(conversation_id: int) -> None:
    conversation_repository.delete_conversation(conversation_id)
    conversation_repository.update_last_update_of_conversation(conversation_id)
