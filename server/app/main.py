from fastapi import FastAPI

from app.routes import user_route, token_route, review_route, conversation_route
from app.utils.db import engine

from app.models import (
    conversations,
    keywords,
    likes,
    messages,
    reviews,
    uk_links,
    users
)

conversations.Base.metadata.create_all(bind=engine)
keywords.Base.metadata.create_all(bind=engine)
likes.Base.metadata.create_all(bind=engine)
messages.Base.metadata.create_all(bind=engine)
reviews.Base.metadata.create_all(bind=engine)
uk_links.Base.metadata.create_all(bind=engine)
users.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_route.router)
app.include_router(token_route.router)
app.include_router(review_route.router)
app.include_router(conversation_route.router)
