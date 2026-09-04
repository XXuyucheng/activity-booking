from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.camp import Camp
    from app.models.schedule import Schedule


class Activity(TimestampMixin, Base):
    """活动。full 由排期推导，不落库。图集/标签/详情段落为 v1.1。"""

    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    camp_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("camps.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(4096), nullable=False, default="")
    cover: Mapped[str] = mapped_column(String(512), nullable=False, default="")
    duration: Mapped[int | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    child_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    notice: Mapped[str] = mapped_column(String(1024), nullable=False, default="")

    camp: Mapped[Camp] = relationship(back_populates="activities")
    schedules: Mapped[list[Schedule]] = relationship(back_populates="activity")
    bookings: Mapped[list[Booking]] = relationship(back_populates="activity")
