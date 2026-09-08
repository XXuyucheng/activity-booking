from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.staff import StaffSession, StaffUser


class StaffUserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, staff_id: uuid.UUID) -> StaffUser | None:
        return self._db.get(StaffUser, staff_id)

    def get_by_username(self, username: str) -> StaffUser | None:
        return self._db.scalar(select(StaffUser).where(StaffUser.username == username))

    def add(self, staff: StaffUser) -> StaffUser:
        self._db.add(staff)
        self._db.flush()
        return staff


class StaffSessionRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, session_id: str) -> StaffSession | None:
        return self._db.get(StaffSession, session_id)

    def add(self, session: StaffSession) -> StaffSession:
        self._db.add(session)
        self._db.flush()
        return session

    def delete(self, session: StaffSession) -> None:
        self._db.delete(session)
        self._db.flush()
