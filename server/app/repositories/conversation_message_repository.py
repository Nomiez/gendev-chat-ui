from datetime import datetime

from app.schemas.message_schema import ConversationMessage, ConversationMessagePut, ReadingState
from app.utils.db import get_db
from app.models import conversation_messages


class ConversationMessageRepository:

    def __init__(self):
        self.db = next(get_db())

    def get_message_by_id(self, message_id: int) -> ConversationMessage:
        message = self.db.query(conversation_messages.ConversationMessage).filter(
            conversation_messages.ConversationMessage.message_id == message_id).first()
        return ConversationMessage(**message.to_dict())

    def get_messages_by_conversation_id_pag(self, conversation_id: int, page: int, size: int) -> list[
        ConversationMessage]:
        conversation_message_list = self.db.query(conversation_messages.ConversationMessage) \
            .filter(conversation_messages.ConversationMessage.conversation_id == conversation_id) \
            .order_by(conversation_messages.ConversationMessage.created_at.desc()) \
            .offset((page - 1) * size) \
            .limit(size) \
            .all()
        return [ConversationMessage(**message.to_dict()) for message in conversation_message_list]

    def create_new_message(self, message: ConversationMessage):
        message = conversation_messages.ConversationMessage(**message.model_dump())
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return ConversationMessage(**message.to_dict())

    def update_conversation_message(self, message_id: int, message: ConversationMessagePut) -> ConversationMessage:
        old_message = self.get_message_by_id(message_id)
        if not old_message:
            raise Exception(f"Message with id {message_id} not found")
        updated_values = message.model_dump(exclude_unset=True)
        for key, value in updated_values.items():
            setattr(old_message, key, value)
        old_message.updated_at = datetime.now()
        message_dict = old_message.model_dump()
        new_message = conversation_messages.ConversationMessage(**message_dict)
        self.db.query(conversation_messages.ConversationMessage).filter(
            conversation_messages.ConversationMessage.message_id == message_id).update(new_message.to_dict())
        self.db.commit()
        return self.get_message_by_id(message_id)

    def update_reading_state_for_conversation(self, conversation_id: int, user_id: int, state: ReadingState):
        if state == ReadingState.RECEIVED:
            self.db.query(conversation_messages.ConversationMessage) \
                .filter(conversation_messages.ConversationMessage.conversation_id == conversation_id) \
                .filter(conversation_messages.ConversationMessage.sender_id == user_id) \
                .filter(conversation_messages.ConversationMessage.received_at == None) \
                .update({conversation_messages.ConversationMessage.received_at: datetime.now()})
        elif state == ReadingState.READ:
            self.db.query(conversation_messages.ConversationMessage) \
                .filter(conversation_messages.ConversationMessage.conversation_id == conversation_id) \
                .filter(conversation_messages.ConversationMessage.sender_id == user_id) \
                .filter(conversation_messages.ConversationMessage.read_at == None) \
                .update({conversation_messages.ConversationMessage.read_at: datetime.now()})

        self.db.commit()


conversation_message_repository = ConversationMessageRepository()
