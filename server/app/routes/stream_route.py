import asyncio
import uuid
from asyncio import Queue
from uuid import UUID

from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse
from starlette.requests import Request

from app.schemas.user_schema import UserSchema
from app.services import auth_service
from app.services.auth_service import is_valid_user
from app.utils.stream_handles import stream_handles as handles

STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milisecond

router = APIRouter(
    tags=['stream']
)


@router.get('/stream')
async def message_stream(user: UserSchema | None = Depends(auth_service.get_current_user)):
    is_valid_user(user)

    # Create new UUID for stream
    stream_uuid: UUID = uuid.uuid4()
    handles.create_handle(user.user_id, stream_uuid)

    # Create event generator
    async def event_generator():
        try:
            while True:
                if not (handles.is_handle_ready(user.user_id, stream_uuid)):
                    yield {
                        "event": "message",
                        "data": handles.dequeue_message(user.user_id, stream_uuid)
                    }

                await asyncio.sleep(STREAM_DELAY)
        except asyncio.CancelledError:
            handles.remove_handle(user.user_id, stream_uuid)

    return EventSourceResponse(event_generator())
