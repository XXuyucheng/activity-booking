from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.activity import Activity
    from app.models.booking import Booking


class Schedule(TimestampMixin, Base):
    """排期：前端某日 + 某时段。库存以 booked_count / capacity 为准。"""

    __tablename__ = "schedules"
    __table_args__ = (
        CheckConstraint("booked_count >= 0", name="booked_nonneg"),
        CheckConstraint("booked_count <= capacity", name="booked_le_capacity"),
        CheckConstraint("end_time > start_time", name="time_order"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("activities.id"),
        nullable=False,
    )
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    booked_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")

    activity: Mapped[Activity] = relationship(back_populates="schedules")
    bookings: Mapped[list[Booking]] = relationship(back_populates="schedule")
