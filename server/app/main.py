from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.models.users import User
from app.utils.db import get_db, engine
from app.repositories.user_repository import user_repository

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


@app.get("/user")
async def get_user():
    return user_repository.get_user_from_username("Test")
