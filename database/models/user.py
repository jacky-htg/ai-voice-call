from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import uuid

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .call import Call

from database.engine import Base

def generate_uuid() -> str:
    return str(uuid.uuid7())

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    calls: Mapped[list["Call"]] = relationship(
        "Call",
        back_populates="caller",
        cascade="all, delete-orphan",
    )
