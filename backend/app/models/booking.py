from __future__ import annotations

import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.activity import Activity
    from app.models.camp import Camp
    from app.models.notification import NotificationLog
    from app.models.schedule import Schedule
    from app.models.user import User


class Booking(TimestampMixin, Base):
    """预约。联系人姓名/手机为当次快照，不只依赖 User。"""

    __tablename__ = "bookings"
    __table_args__ = (
        CheckConstraint("adult_count >= 1", name="adult_min"),
        CheckConstraint("child_count >= 0", name="child_nonneg"),
        CheckConstraint("unpaid_amount >= 0", name="unpaid_nonneg"),
        CheckConstraint("unpaid_amount <= total_price", name="unpaid_lte_total"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    camp_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("camps.id"),
        nullable=False,
    )
    activity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("activities.id"),
        nullable=False,
    )
    schedule_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schedules.id"),
        nullable=False,
    )
    contact_name: Mapped[str] = mapped_column(String(64), nullable=False)
    contact_phone: Mapped[str] = mapped_column(String(20), nullable=False)
    adult_count: Mapped[int] = mapped_column(Integer, nullable=False)
    child_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    remark: Mapped[str] = mapped_column(String(512), nullable=False, default="")
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    unpaid_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")

    user: Mapped[User] = relationship(back_populates="bookings")
    camp: Mapped[Camp] = relationship(back_populates="bookings")
    activity: Mapped[Activity] = relationship(back_populates="bookings")
    schedule: Mapped[Schedule] = relationship(back_populates="bookings")
    notification_logs: Mapped[list[NotificationLog]] = relationship(
        back_populates="booking",
    )
