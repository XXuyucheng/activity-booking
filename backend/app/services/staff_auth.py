from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.exceptions import AuthError, NotFoundError
from app.core.security import verify_password
from app.models.staff import StaffSession, StaffUser
from app.repositories.camp import CampRepository
from app.repositories.staff import StaffUserRepository
from app.schemas.staff import StaffMeResponse
from app.services.staff_session import StaffSessionService


@dataclass(frozen=True)
class StaffLoginResult:
    session: StaffSession
    staff: StaffUser


class StaffAuthService:
    def __init__(self, db: Session, settings: Settings | None = None) -> None:
        self._db = db
        self._settings = settings or get_settings()
        self._staff = StaffUserRepository(db)
        self._camps = CampRepository(db)
        self._sessions = StaffSessionService(db, self._settings)

    def login(self, username: str, password: str) -> StaffLoginResult:
        staff = self._staff.get_by_username(username)
        hashed = staff.password_hash if staff is not None else None
        if not verify_password(password, hashed) or staff is None or not staff.is_active:
            raise AuthError("invalid credentials", status_code=401)
        session = self._sessions.issue(staff.id)
        self._db.commit()
        return StaffLoginResult(session=session, staff=staff)

    def logout(self, session_id: str | None) -> None:
        self._sessions.revoke(session_id)
        self._db.commit()

    def current_staff(self, session_id: str | None) -> StaffUser | None:
        session = self._sessions.get_valid(session_id)
        if session is None:
            self._db.commit()
            return None
        staff = self._staff.get_by_id(session.staff_user_id)
        if staff is None or not staff.is_active:
            self._sessions.revoke(session.id)
            self._db.commit()
            return None
        return staff

    def me_response(self, staff: StaffUser) -> StaffMeResponse:
        camp = self._camps.get_by_id(staff.camp_id)
        if camp is None:
            raise NotFoundError("camp not found")
        return StaffMeResponse(
            id=staff.id,
            username=staff.username,
            camp_id=staff.camp_id,
            camp_slug=camp.slug,
            camp_name=camp.name,
        )
