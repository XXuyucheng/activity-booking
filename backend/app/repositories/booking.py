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

    def list_by_user_id(self, user_id: uuid.UUID) -> list[Booking]:
        stmt = (
            select(Booking)
            .where(Booking.user_id == user_id)
            .order_by(Booking.created_at.desc())
        )
        return list(self._db.scalars(stmt))

    def has_for_activity(self, activity_id: uuid.UUID) -> bool:
        stmt = select(Booking.id).where(Booking.activity_id == activity_id).limit(1)
        return self._db.scalar(stmt) is not None

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
