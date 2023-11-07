from app.utils.db import get_db


class ThreadMessageRepository:

    def __init__(self):
        self.db = next(get_db())


thread_message_repository = ThreadMessageRepository()
