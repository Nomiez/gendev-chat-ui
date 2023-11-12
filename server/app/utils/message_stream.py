import re
from datetime import datetime

import phonenumbers

from app.models.conversation_messages import SenderType
from app.models.conversations import State
from app.schemas.conversation_schema import ConversationSchema
from app.schemas.message_schema import ConversationMessage


class MessageStream:
    def __init__(self, elements: list[ConversationMessage]):
        self.elements = elements

    @staticmethod
    def _extract_phone_numbers(text):
        numbers = []
        for match in phonenumbers.PhoneNumberMatcher(text, None):
            numbers.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
        print(numbers)
        return numbers

    @staticmethod
    def _censor_phone_numbers(text):

        phone_number_pattern = re.compile(r'(\(?([\d \-\)\–\+\/\(]+){6,}\)?([ .\-–\/]?)([\d]+))')
        censored_text = re.sub(phone_number_pattern, "[TELEFONNUMMER]", text)

        return censored_text

    @staticmethod
    def _censor_email_addresses(text):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        censored_text = re.sub(email_pattern, "[EMAIL]", text)
        return censored_text

    @staticmethod
    def _censor_url(text):
        # Define a regular expression pattern to match the sensitive part of the URL
        pattern = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
        # Use regular expression substitution to censor the URL
        censored_text = re.sub(pattern, "[LINK]", text)
        return censored_text

    @staticmethod
    def _internal_censor_function(el):
        el.text = \
            MessageStream._censor_url(
                MessageStream._censor_email_addresses(
                    MessageStream._censor_phone_numbers(el.text)))
        return el

    @staticmethod
    def censor_func(conversation: ConversationSchema):
        if conversation.state == State.ACCEPTED:
            return lambda msg: msg
        else:
            return lambda msg: MessageStream._internal_censor_function(msg)

    @staticmethod
    def hidden_filter(conversation: ConversationSchema, user_id: int):
        user_sender_type = SenderType.CUSTOMER if conversation.customer_id == user_id else SenderType.SERVICE_PROVIDER
        return lambda \
                msg: False if msg.hidden_at is not None \
                              and msg.hidden_at > datetime.now() \
                              and msg.sender_type != user_sender_type else True

    def filter(self, function):
        result = []
        for el in self.elements:
            if function(el) is True:
                result.append(el)
        self.elements = result
        return self

    def map(self, function):
        res = []
        for el in self.elements:
            el = function(el)
            res.append(el)
        self.elements = res
        return self

    def to_list(self):
        return self.elements
