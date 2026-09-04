from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.schedule import Schedule


class ScheduleRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_open_by_activity_id(self, activity_id: uuid.UUID) -> list[Schedule]:
        stmt = (
            select(Schedule)
            .where(Schedule.activity_id == activity_id, Schedule.status == "open")
            .order_by(Schedule.start_time)
        )
        return list(self._db.scalars(stmt))

    def get_by_id(self, schedule_id: uuid.UUID) -> Schedule | None:
        return self._db.get(Schedule, schedule_id)

    def get_by_id_for_update(self, schedule_id: uuid.UUID) -> Schedule | None:
        stmt = select(Schedule).where(Schedule.id == schedule_id).with_for_update()
        return self._db.scalar(stmt)

    def add_booked(self, schedule: Schedule, delta: int) -> None:
        schedule.booked_count += delta
        if schedule.booked_count < 0:
            schedule.booked_count = 0
