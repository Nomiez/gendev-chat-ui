from datetime import datetime
from enum import Enum
from typing import Optional, List
from emoji import is_emoji

from fastapi import APIRouter, Query, Depends, HTTPException, UploadFile, File, Form
from starlette import status
from starlette.responses import FileResponse

from app.models.conversations import State, StateReduced
from app.schemas.user_schema import UserSchema
from app.services import auth_service
from app.services.auth_service import is_valid_user
from app.services.conversation_message_service import get_messages_by_conversation_id_pag, create_new_message, \
    accept_quote, update_message_reactions, get_message_by_message_id, reject_quote
from app.schemas.message_schema import ConversationMessage, ConversationMessagePost

router = APIRouter(
    prefix="/conversation",
    tags=['Message']
)


@router.get("/{conversation_id}/message/", response_model=list[ConversationMessage])
async def get_conversation_message_pag(conversation_id: int,
                                       user: UserSchema | None = Depends(auth_service.get_current_user),
                                       page: int = Query(1),
                                       size: int = Query(12)):
    is_valid_user(user)
    conversations = get_messages_by_conversation_id_pag(conversation_id, user.user_id, page, size)
    return conversations


@router.post("/{conversation_id}/message/", status_code=status.HTTP_201_CREATED, response_model=ConversationMessage)
def post_conversation_message(
        conversation_id: int,
        text: str = Form(...),
        hidden_at: Optional[datetime] = Form(None),
        user: UserSchema | None = Depends(auth_service.get_current_user)):
    is_valid_user(user)
    return create_new_message(conversation_id, user.user_id, ConversationMessagePost(text=text, hidden_at=hidden_at))


@router.post("/{conversation_id}/message/media", status_code=status.HTTP_201_CREATED,
             response_model=ConversationMessage)
def post_conversation_message(
        conversation_id: int,
        text: str = Form(...),
        hidden_at: Optional[datetime] = Form(None),
        media: UploadFile = File(...),
        user: UserSchema | None = Depends(auth_service.get_current_user)):
    is_valid_user(user)
    return create_new_message(conversation_id, user.user_id, ConversationMessagePost(text=text, hidden_at=hidden_at),
                              media)


@router.get("/{conversation_id}/message/{message_id}/media", response_class=FileResponse)
def get_image(conversation_id: int, message_id: int, user: UserSchema | None = Depends(auth_service.get_current_user)):
    is_valid_user(user)
    message = get_message_by_message_id(message_id, conversation_id, user.user_id)
    return FileResponse(path=f"media/conversations/{conversation_id}/{message.message_attachment}",
                        filename=message.message_attachment[64:])


@router.post("/{conversation_id}/message/quote", status_code=status.HTTP_201_CREATED,
             response_model=ConversationMessage)
def post_conversation_message_and_quote_change(
        conversation_id: int,
        text: str = Form(...),
        quote: StateReduced = Form(...),
        user: UserSchema | None = Depends(auth_service.get_current_user)):
    is_valid_user(user)

    if quote.value == State.ACCEPTED.value:
        accept_quote(conversation_id, user.user_id)
    if quote.value == State.REJECTED.value:
        reject_quote(conversation_id, user.user_id)


@router.post("/{conversation_id}/message/{message_id}/reaction", status_code=status.HTTP_201_CREATED,
             response_model=ConversationMessage)
def post_change_raction_from_message(
        conversation_id: int,
        message_id: int,
        emoji: str = Form(...),
        user: UserSchema | None = Depends(auth_service.get_current_user)):
    is_valid_user(user)
    if not is_emoji(emoji) and emoji != " ":
        raise HTTPException(status_code=400, detail="Invalid emoji")
    else:
        return update_message_reactions(conversation_id, message_id, user.user_id, emoji)
