from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.security import new_session_id
from app.models.staff import StaffSession
from app.repositories.staff import StaffSessionRepository


class StaffSessionService:
    def __init__(self, db: Session, settings: Settings | None = None) -> None:
        self._repo = StaffSessionRepository(db)
        self._settings = settings or get_settings()

    def issue(self, staff_user_id: uuid.UUID) -> StaffSession:
        now = datetime.now(UTC)
        session = StaffSession(
            id=new_session_id(),
            staff_user_id=staff_user_id,
            expires_at=now + timedelta(seconds=self._settings.session_ttl_seconds),
        )
        return self._repo.add(session)

    def get_valid(self, session_id: str | None) -> StaffSession | None:
        if not session_id:
            return None
        session = self._repo.get_by_id(session_id)
        if session is None:
            return None
        if session.expires_at <= datetime.now(UTC):
            self._repo.delete(session)
            return None
        return session

    def revoke(self, session_id: str | None) -> None:
        if not session_id:
            return
        session = self._repo.get_by_id(session_id)
        if session is not None:
            self._repo.delete(session)
