from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity import Activity


class ActivityRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, activity_id: uuid.UUID) -> Activity | None:
        return self._db.get(Activity, activity_id)

    def list_open_by_camp_id(self, camp_id: uuid.UUID) -> list[Activity]:
        stmt = (
            select(Activity)
            .where(Activity.camp_id == camp_id, Activity.status == "open")
            .order_by(Activity.created_at)
        )
        return list(self._db.scalars(stmt))

    def list_by_camp_id(self, camp_id: uuid.UUID) -> list[Activity]:
        stmt = (
            select(Activity)
            .where(Activity.camp_id == camp_id)
            .order_by(Activity.created_at)
        )
        return list(self._db.scalars(stmt))
