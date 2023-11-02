from fastapi import APIRouter, Query, Depends, HTTPException
from starlette import status

from app.schemas.conversation_schema import ConversationGet, ConversationPost
from app.schemas.user_schema import UserSchema
from app.services import auth_service
from app.services.auth_service import is_valid_user
from app.services.conversation_service import (
    create_conversation,
    get_conversation_by_id,
    get_conversations_from_user_by_id_pag,
    delete_conversation as remove_conversation
)

router = APIRouter(
    prefix="/conversation",
    tags=['Conversation']
)


@router.get("/", response_model=list[ConversationGet])
async def get_conversations_pag(user: UserSchema | None = Depends(auth_service.get_current_user), page: int = Query(1),
                                size: int = Query(12)):
    is_valid_user(user)
    return get_conversations_from_user_by_id_pag(user.user_id, page, size)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ConversationGet)
async def post_conversation(conversation: ConversationPost,
                            user: UserSchema | None = Depends(auth_service.get_current_user)):
    is_valid_user(user)
    if conversation.customer_id != user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to create this resource")
    return create_conversation(conversation)


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(conversation_id: int,
                        user: UserSchema | None = Depends(auth_service.get_current_user)):
    is_valid_user(user)
    conversation_to_delete = get_conversation_by_id(conversation_id)
    if (conversation_to_delete.customer_id != user.user_id) and (
            get_conversation_by_id(conversation_id).service_provider_id != user.user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to delete this resource")
    if conversation_to_delete.deleted_at is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resource already deleted")
    remove_conversation(conversation_id)
