from fastapi import FastAPI

from app.routes import user_route, token_route, review_route, conversation_route, conversation_message_route, \
    stream_route
from app.utils.db import engine

from app.models import (
    conversations,
    keywords,
    likes,
    conversation_messages,
    reviews,
    uk_links,
    users, thread_messages
)

conversations.Base.metadata.create_all(bind=engine)
keywords.Base.metadata.create_all(bind=engine)
likes.Base.metadata.create_all(bind=engine)
conversation_messages.Base.metadata.create_all(bind=engine)
thread_messages.Base.metadata.create_all(bind=engine)
reviews.Base.metadata.create_all(bind=engine)
uk_links.Base.metadata.create_all(bind=engine)
users.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_route.router)
app.include_router(token_route.router)
app.include_router(review_route.router)
app.include_router(conversation_route.router)
app.include_router(conversation_message_route.router)
app.include_router(stream_route.router)
