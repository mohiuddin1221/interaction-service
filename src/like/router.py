from typing import List
from fastapi import APIRouter, FastAPI, Depends, Header, HTTPException, status
import redis.asyncio as redis
from src.common.utils import get_current_user
from database import get_async_db, get_redis
from .schemas import LikeCreate


router = APIRouter(prefix="/like", tags=["Like"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_like(
    like_data: LikeCreate,
    current_user: dict = Depends(get_current_user),
    r: redis = Depends(get_redis),
):
    user_uid = current_user["user_uid"]
    username = current_user["username"]
    post_uid = like_data.post_uid

    post_key = f"post:{post_uid}:likes"
    like_value = f"{user_uid}:{username}"

    is_liked = await r.sismember(post_key, like_value)

    if is_liked:
        await r.srem(post_key, like_value)
        return {"message": "Post unliked successfully."}

    else:
        await r.sadd(post_key, like_value)
        return {"message": "Post liked successfully."}

    # Check if the user has already liked the post
