import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from starlette import status

from app.models.conversations import State
from app.models.conversation_messages import SenderType, MessageType
from app.repositories.conversation_message_repository import conversation_message_repository
from app.repositories.conversation_repository import conversation_repository
from app.schemas.conversation_schema import ConversationSchema
from app.utils.stream_handles import stream_handles as handles

from app.schemas.message_schema import ConversationMessage, ConversationMessagePost, ConversationMessagePostInternal, \
    ReadingState, ConversationMessagePut
from app.utils.message_stream import MessageStream


def get_messages_by_conversation_id_pag(conversation_id: int, user_id, page: int, size: int) -> list[
    ConversationMessage]:
    conversation = conversation_repository.get_conversation_by_id(conversation_id)

    # Check if conversations exists
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    # Check which part the user is in the conversations
    if (conversation.customer_id != user_id) and (conversation.service_provider_id != user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not in conversations")

    # Check if conversations is deleted
    if conversation.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    messages = conversation_message_repository.get_messages_by_conversation_id_pag(conversation_id, page, size)

    _update_conversation_reading_state(conversation, user_id)

    return MessageStream(messages) \
        .filter(lambda msg: msg is not None) \
        .filter(MessageStream.hidden_filter(conversation, user_id)) \
        .map(MessageStream.censor_func(conversation)) \
        .to_list()


def _save_file(file: UploadFile, filename: str, conversation_id: int) -> None:
    try:
        contents = file.file.read()
        os.makedirs(os.path.dirname(f"media/conversations/{conversation_id}/"), exist_ok=True)
        with open(f"media/conversations/{conversation_id}/{filename}", "xb") as f:
            f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error saving file: {str(e)}")
    finally:
        file.file.close()


def create_new_message(conversation_id: int,
                       user_id: int,
                       message: ConversationMessagePost,
                       file: Optional[UploadFile] = None) -> ConversationMessage:
    message = ConversationMessagePostInternal(**message.model_dump())
    conversation = conversation_repository.get_conversation_by_id(conversation_id)

    # Check if conversations exists
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    # Check which part the user is in the conversations
    if (conversation.customer_id != user_id) and (conversation.service_provider_id != user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not in conversations")

    # Check if conversations is deleted
    if conversation.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    # Check if conversations is rejected
    if conversation.state == State.REJECTED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Conversation is rejected")

    if conversation.customer_id == user_id:
        message.sender_type = SenderType.CUSTOMER
    else:
        message.sender_type = SenderType.SERVICE_PROVIDER

    message.conversation_id = conversation_id

    # Check if message has attachment (image or pdf)
    if file is not None and file.content_type in ['image/jpeg', 'image/png', 'application/pdf']:
        filename = f"{str(uuid.uuid4())}{file.filename}"
        _save_file(file, filename, conversation_id)
        message.message_attachment = filename

    # Check current message state
    last_message = conversation_message_repository.get_messages_by_conversation_id_pag(conversation_id, 1, 1)
    if (last_message == []) and (message.sender_type == SenderType.CUSTOMER):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="First message must be sent by service provider")

    if not last_message:
        message.message_type = MessageType.QUOTE_OFFER
    else:
        message.message_type = MessageType.STANDARD_MESSAGE

    new_message = conversation_message_repository.create_new_message(message)

    conversation_repository.update_last_update_of_conversation(conversation_id)

    dict_message = {
        "conversation_id": conversation_id
    }
    handles.enqueue_message_opt([user_id, (conversation.customer_id
                                           if conversation.customer_id is not user_id
                                           else conversation.service_provider_id)], str(dict_message))

    return new_message


def accept_quote(conversation_id: int, user_id: int) -> None:
    conversation = conversation_repository.get_conversation_by_id(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    if (conversation.customer_id != user_id) and (conversation.service_provider_id != user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not in conversations")

    if conversation.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    if conversation.state != State.QUOTED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Conversation is already accepted or rejected")

    if conversation.customer_id != user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Only customer can accept quote")

    conversation_message_repository.create_new_message(ConversationMessagePostInternal(
        text=f"Quote accepted by customer!",
        conversation_id=conversation_id,
        sender_type=SenderType.CUSTOMER,
        message_type=MessageType.ACCEPT_QUOTE_MESSAGE,
    ))
    conversation_repository.update_state_of_conversation(conversation_id, user_id, State.ACCEPTED)
    conversation_repository.update_last_update_of_conversation(conversation_id)

    dict_message = {
        "conversation_id": conversation_id
    }
    handles.enqueue_message_opt([user_id], str(dict_message))


def reject_quote(conversation_id: int, user_id: int) -> None:
    conversation = conversation_repository.get_conversation_by_id(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    if (conversation.customer_id != user_id) and (conversation.service_provider_id != user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not in conversations")

    if conversation.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    if conversation.state != State.QUOTED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Conversation is already accepted or rejected")

    conversation_message_repository.create_new_message(ConversationMessagePostInternal(
        text=f"Quote rejected by customer!",
        conversation_id=conversation_id,
        sender_type=SenderType.CUSTOMER,
        message_type=MessageType.REJECT_QUOTE_MESSAGE,
    ))
    conversation_repository.update_state_of_conversation(conversation_id, user_id, State.REJECTED)
    conversation_repository.update_last_update_of_conversation(conversation_id)

    dict_message = {
        "conversation_id": conversation_id
    }
    handles.enqueue_message_opt([user_id], str(dict_message))


def update_sending_status_by_conversation_id(conversation_id: int,
                                             receiver_id: int,
                                             sender_id: int,
                                             state: ReadingState) -> None:
    last_message = conversation_message_repository.get_messages_by_conversation_id_pag(conversation_id, 1, 1)
    if last_message is not [] and last_message[0].read_at is not None:
        return
    conversation_message_repository.update_reading_state_for_conversation(conversation_id, receiver_id, state)
    handles.enqueue_message_opt([sender_id], str({"conversation_id": conversation_id}))


def get_message_by_message_id(message_id: int, conversation_id: int, user_id: int,
                              censored: bool = False) -> ConversationMessage:
    message = conversation_message_repository.get_message_by_id(message_id)
    conversation = conversation_repository.get_conversation_by_id(conversation_id)

    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    if (conversation.customer_id != user_id) and (conversation.service_provider_id != user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not in conversations")

    if conversation.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    if not censored:
        msg = MessageStream([message]) \
            .filter(lambda msg: msg is not None) \
            .filter(MessageStream.hidden_filter(conversation, user_id)) \
            .to_list()
        return msg[0] if len(msg) > 0 else None
    else:
        return MessageStream([message]) \
            .filter(lambda msg: msg is not None) \
            .filter(MessageStream.hidden_filter(conversation, user_id)) \
            .map(MessageStream.censor_func(conversation)) \
            .to_list()[0]


def update_message_reactions(conversation_id: int, message_id, user_id: int, reaction: str) -> ConversationMessage:
    conversation = conversation_repository.get_conversation_by_id(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    if (conversation.customer_id != user_id) and (conversation.service_provider_id != user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not in conversations")

    if conversation.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Conversation with id {conversation_id} not found")

    if conversation.state != State.QUOTED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Conversation is already accepted or rejected")

    msg = conversation_message_repository.get_message_by_id(message_id)
    if conversation.customer_id == user_id:
        msg.customer_reaction = reaction
    else:
        msg.service_provider_reaction = reaction
    result = conversation_message_repository.update_conversation_message(msg.message_id,
                                                                         ConversationMessagePut(**msg.model_dump()))
    conversation_repository.update_last_update_of_conversation(conversation_id)
    # handles.enqueue_message_opt([user_id], str({"conversation_id": conversation_id}))
    return result


def _update_conversation_reading_state(conversation: ConversationSchema, user_id: int) -> None:
    # Update read state of the messages to received
    if conversation.customer_id == user_id:
        update_sending_status_by_conversation_id(conversation.conversation_id,
                                                 user_id,
                                                 conversation.customer_id,
                                                 ReadingState.READ)
    elif conversation.service_provider_id == user_id:
        update_sending_status_by_conversation_id(conversation.conversation_id,
                                                 user_id,
                                                 conversation.service_provider_id,
                                                 ReadingState.READ)
