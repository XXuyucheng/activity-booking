from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.session import Session as AuthSession


class SessionRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, session_id: str) -> AuthSession | None:
        return self._db.get(AuthSession, session_id)

    def add(self, session: AuthSession) -> AuthSession:
        self._db.add(session)
        self._db.flush()
        return session

    def delete(self, session: AuthSession) -> None:
        self._db.delete(session)
        self._db.flush()
