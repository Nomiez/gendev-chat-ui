from datetime import datetime

from sqlalchemy import or_

from app.models.conversations import Conversation
from app.schemas.conversation_schema import ConversationGet, ConversationPost, ConversationSchema
from app.utils.db import get_db


class ConversationRepository:
    def __init__(self):
        self.db = next(get_db())

    def get_conversation_by_id(self, conversation_id: int) -> ConversationSchema:
        conversation = self.db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
        return ConversationSchema(**conversation.to_dict())

    def get_conversations_by_user_id_pag(self, user_id: int, page: int, size: int) -> list[ConversationGet]:
        conversation_list = self.db.query(Conversation) \
            .filter(or_(Conversation.customer_id == user_id, Conversation.service_provider_id == user_id)) \
            .filter(Conversation.deleted_at == None) \
            .order_by(Conversation.updated_at.desc()) \
            .offset((page - 1) * size) \
            .limit(size).all()

        return [ConversationGet(**conversation.to_dict()) for conversation in conversation_list]

    def create_conversation(self, conversation: ConversationPost) -> ConversationGet:
        new_conversation = Conversation(customer_id=conversation.customer_id,
                                        service_provider_id=conversation.service_provider_id)
        self.db.add(new_conversation)
        self.db.commit()
        self.db.refresh(new_conversation)
        return ConversationGet(**new_conversation.to_dict())

    def delete_conversation(self, conversation_id: int) -> None:
        conversation = self.db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
        conversation.deleted_at = datetime.now()
        self.db.commit()
        self.db.refresh(conversation)


conversation_repository = ConversationRepository()
