from typing import List
from fastapi import APIRouter, FastAPI, Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncIterable, Iterable
from fastapi.sse import EventSourceResponse
import asyncio
import json
from fastapi import BackgroundTasks


from database import get_async_db
from .schemas import CommentCreate, CommentResponse
from .service import (
    create_user_comment,
)
from .token import decode_user_token


router = APIRouter(prefix="/comment", tags=["Comment"])

active_connections: List[asyncio.Queue] = []


async def broadcast_to_all(message: str):
    for queue in active_connections:
        await queue.put(message)


@router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_async_db),
    authorization: str = Header(...),
):
    try:
        user_uid, username = decode_user_token(authorization)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid User UID format")

    response_data = await create_user_comment(comment_data, db, user_uid, username)
    comment_response = CommentResponse.model_validate(response_data)
    background_tasks.add_task(broadcast_to_all, comment_response)

    return response_data


@router.get("/stream/comments", response_class=EventSourceResponse)
async def stream_comments() -> AsyncIterable[CommentResponse]:
    user_queue = asyncio.Queue()
    active_connections.append(user_queue)

    try:
        while True:
            data: CommentResponse = await user_queue.get()

            yield data

    except asyncio.CancelledError:
        active_connections.remove(user_queue)
