from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import NotificationLog

_TERMINAL = ("sent", "skipped")


class NotificationRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def add(self, log: NotificationLog) -> NotificationLog:
        self._db.add(log)
        self._db.flush()
        return log

    def has_terminal(self, booking_id: uuid.UUID, kind: str) -> bool:
        stmt = (
            select(NotificationLog.id)
            .where(
                NotificationLog.booking_id == booking_id,
                NotificationLog.type == kind,
                NotificationLog.status.in_(_TERMINAL),
            )
            .limit(1)
        )
        return self._db.scalar(stmt) is not None
