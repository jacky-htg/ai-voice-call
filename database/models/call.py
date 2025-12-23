from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .user import User
    from .session import Session

import uuid
from database.engine import Base

def generate_uuid() -> str:
    return str(uuid.uuid7())    

class Call(Base):
    __tablename__ = "calls"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    caller_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    caller: Mapped["User"] = relationship("User", back_populates="calls")
    sessions: Mapped[list["Session"]] = relationship("Session", back_populates="call", cascade="all, delete-orphan")