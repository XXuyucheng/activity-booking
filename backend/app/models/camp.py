from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.activity import Activity
    from app.models.booking import Booking
    from app.models.staff import StaffUser


class Camp(TimestampMixin, Base):
    """营地。slug 用于多营地 URL。location/story/设施/套票为 v1.1。"""

    __tablename__ = "camps"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(2048), nullable=False, default="")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="draft")

    activities: Mapped[list[Activity]] = relationship(back_populates="camp")
    bookings: Mapped[list[Booking]] = relationship(back_populates="camp")
    staff_users: Mapped[list[StaffUser]] = relationship(back_populates="camp")
