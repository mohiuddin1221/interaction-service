import uuid
from typing import Optional, List
from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    post_uid: uuid.UUID = Field(
        ..., description="The UID of the post being commented on"
    )
    content: str = Field(..., description="The content of the comment")
    parent_uid: Optional[uuid.UUID] = Field(
        None, description="The UID of the parent comment if this is a reply"
    )


class CommentResponse(BaseModel):
    id: int
    uid: uuid.UUID
    post_uid: uuid.UUID
    content: str
    parent_uid: Optional[uuid.UUID] = None
    user_uid: uuid.UUID
    username: str
    created_at: str
    updated_at: str
