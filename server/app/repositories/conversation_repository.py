from datetime import datetime

from sqlalchemy import or_

from app.models.conversations import Conversation, State
from app.repositories.conversation_message_repository import conversation_message_repository
from app.schemas.conversation_schema import ConversationGet, ConversationPost, ConversationSchema
from app.utils.db import get_db


class ConversationRepository:
    def __init__(self):
        self.db = next(get_db())

    def get_conversation_by_id(self, conversation_id: int) -> ConversationSchema | None:
        conversation = self.db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
        if not conversation:
            return None
        return ConversationSchema(**conversation.to_dict())

    def get_conversations_by_user_id_pag(self, user_id: int, page: int, size: int) -> list[ConversationGet]:
        conversation_list = self.db.query(Conversation) \
            .filter(or_(Conversation.customer_id == user_id, Conversation.service_provider_id == user_id)) \
            .filter(Conversation.deleted_at == None) \
            .order_by(Conversation.updated_at.desc()) \
            .offset((page - 1) * size) \
            .limit(size).all()
        # Insert first message of each conversations
        last_message_list = []
        for conversation in conversation_list:
            conversation_msg_list = conversation_message_repository.get_messages_by_conversation_id_pag(
                conversation.conversation_id, 1, 1)
            last_message_list.append(None if conversation_msg_list == [] else conversation_msg_list[0])

        return [ConversationGet(**conversation.to_dict(), last_message=last_msg) for conversation, last_msg in
                zip(conversation_list, last_message_list)]

    def create_conversation(self, conversation: ConversationPost) -> ConversationGet:
        new_conversation = Conversation(customer_id=conversation.customer_id,
                                        service_provider_id=conversation.service_provider_id)
        self.db.add(new_conversation)
        self.db.commit()
        self.db.refresh(new_conversation)
        return ConversationGet(**new_conversation.to_dict(), last_message=None)

    def delete_conversation(self, conversation_id: int) -> None:
        conversation = self.db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
        conversation.deleted_at = datetime.now()
        self.db.commit()
        self.db.refresh(conversation)

    def update_state_of_conversation(self, conversation_id: int, state: State) -> ConversationGet:
        conversation = self.db.query(Conversation).filter(Conversation.conversation_id == conversation_id).first()
        conversation.state = state
        self.db.commit()
        self.db.refresh(conversation)
        return ConversationGet(**conversation.to_dict())


conversation_repository = ConversationRepository()
