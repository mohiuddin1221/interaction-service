from fastapi import HTTPException
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from .models import Comment


async def create_user_comment(comment_data, db, user_uid, username):
    try:
        new_comment = Comment(
            post_uid=comment_data.post_uid,
            content=comment_data.content,
            username=username,
            user_uid=user_uid,
            parent_uid=comment_data.parent_uid,
        )
        db.add(new_comment)
        await db.commit()
        await db.refresh(new_comment)
        return new_comment

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500, detail=f"Comment toiri korte somossa: {str(e)}"
        )
