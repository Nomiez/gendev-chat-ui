from asyncio import Queue
from uuid import UUID

import asyncio


class StreamHandles:
    def __init__(self):
        self._handles: dict[int, dict[UUID, Queue[str]]] = {}

    def create_handle(self, user_id: int, stream_uuid: UUID) -> None:
        if user_id not in self._handles:
            self._handles.update({user_id: {stream_uuid: Queue()}})
        else:
            self._handles.get(user_id).update({stream_uuid: Queue()})

    def _get_handle(self, user_id: int, stream_uuid: UUID) -> Queue:
        return self._handles.get(user_id).get(stream_uuid)

    def remove_handle(self, user_id: int, stream_uuid: UUID) -> None:
        self._handles.get(user_id).pop(stream_uuid)
        if len(self._handles.get(user_id)) == 0:
            self._handles.pop(user_id)

    def is_handle_ready(self, user_id: int, stream_uuid: UUID) -> bool:
        return self._get_handle(user_id, stream_uuid).empty()

    def enqueue_message_opt(self, user_id: int, message: str):
        if user_id in self._handles:
            for stream in self._handles.get(user_id).values():
                stream.put_nowait(message)

    def dequeue_message(self, user_id: int, stream_uuid: UUID):
        return self._get_handle(user_id, stream_uuid).get_nowait()


stream_handles = StreamHandles()
