import uuid
import datetime
from typing import Optional, List
from sqlalchemy import String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, index=True, unique=True, nullable=False
    )

    post_uid: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    username: Mapped[str] = mapped_column(String(50), nullable=False)
    user_uid: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)

    # parent_uid: if its main comment its must be null and if its reply then its be main comment id
    parent_uid: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("comments.uid"), index=True, nullable=True
    )

    replies: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="parent",
        cascade="all, delete-orphan",
        order_by="Comment.created_at.asc()",
    )

    parent: Mapped[Optional["Comment"]] = relationship(
        "Comment",
        back_populates="replies",
        remote_side=[uid],
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.datetime.now,
        server_default=func.now(),
        onupdate=func.now(),
    )
