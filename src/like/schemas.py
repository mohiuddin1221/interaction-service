import uuid
from typing import Optional, List
from pydantic import BaseModel, Field

class LikeCreate(BaseModel):
    post_uid: uuid.UUID = Field(
        ..., description="The UID of the post being liked"
    )

