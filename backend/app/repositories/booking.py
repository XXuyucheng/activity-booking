from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.schedule import Schedule


class BookingRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def add(self, booking: Booking) -> Booking:
        self._db.add(booking)
        self._db.flush()
        return booking

    def get_by_id(self, booking_id: uuid.UUID) -> Booking | None:
        return self._db.get(Booking, booking_id)

    def list_by_user_id(
        self,
        user_id: uuid.UUID,
        camp_id: uuid.UUID | None = None,
    ) -> list[Booking]:
        stmt = select(Booking).where(Booking.user_id == user_id)
        if camp_id is not None:
            stmt = stmt.where(Booking.camp_id == camp_id)
        stmt = stmt.order_by(Booking.created_at.desc())
        return list(self._db.scalars(stmt))

    def list_by_camp_id(
        self,
        camp_id: uuid.UUID,
        status: str | None = None,
    ) -> list[Booking]:
        stmt = select(Booking).where(Booking.camp_id == camp_id)
        if status is not None:
            stmt = stmt.where(Booking.status == status)
        stmt = stmt.order_by(Booking.created_at.desc())
        return list(self._db.scalars(stmt))

    def has_for_activity(self, activity_id: uuid.UUID) -> bool:
        stmt = select(Booking.id).where(Booking.activity_id == activity_id).limit(1)
        return self._db.scalar(stmt) is not None

    def list_active_by_schedule_ids(
        self,
        schedule_ids: list[uuid.UUID],
    ) -> list[Booking]:
        if not schedule_ids:
            return []
        stmt = (
            select(Booking)
            .where(
                Booking.schedule_id.in_(schedule_ids),
                Booking.status != "expired",
            )
            .order_by(Booking.created_at)
        )
        return list(self._db.scalars(stmt))

    def list_pending_starting_between(
        self,
        window_start: datetime,
        window_end: datetime,
    ) -> list[Booking]:
        stmt = (
            select(Booking)
            .join(Schedule, Booking.schedule_id == Schedule.id)
            .where(
                Booking.status == "pending",
                Schedule.start_time > window_start,
                Schedule.start_time <= window_end,
            )
            .order_by(Schedule.start_time)
        )
        return list(self._db.scalars(stmt))
