import uuid
import datetime
from typing import Optional, List
from sqlalchemy import String, ForeignKey, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class PostLike(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uid: Mapped[uuid.UUID] = mapped_column(
        default=uuid.uuid4, index=True, unique=True, nullable=False
    )

    post_uid: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)
    user_uid: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)

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
