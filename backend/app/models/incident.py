from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.core.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    requester: Mapped[str] = mapped_column(String(150), nullable=False)
    area: Mapped[str] = mapped_column(String(100), nullable=False)

    category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="aberto",
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(50),
        default="media",
        nullable=False,
    )

    impact_users: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    urgency: Mapped[str] = mapped_column(
        String(50),
        default="media",
        nullable=False,
    )

    ai_category: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    ai_priority: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    ai_confidence: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
