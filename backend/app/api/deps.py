"""HTTP 依赖：数据库会话、Cookie 中的 session id、当前用户。"""

from collections.abc import Generator

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.db import db_session
from app.core.exceptions import AuthError
from app.models.staff import StaffUser
from app.models.user import User
from app.services.auth import AuthService
from app.services.staff_auth import StaffAuthService


def get_db() -> Generator[Session, None, None]:
    yield from db_session()


def get_session_id(request: Request) -> str | None:
    return request.cookies.get(get_settings().session_cookie_name)


def get_staff_session_id(request: Request) -> str | None:
    return request.cookies.get(get_settings().admin_session_cookie_name)


def get_current_user(
    db: Session = Depends(get_db),
    session_id: str | None = Depends(get_session_id),
) -> User:
    user = AuthService(db).current_user(session_id)
    if user is None:
        raise AuthError("not logged in", status_code=401)
    return user


def get_current_staff(
    db: Session = Depends(get_db),
    session_id: str | None = Depends(get_staff_session_id),
) -> StaffUser:
    staff = StaffAuthService(db).current_staff(session_id)
    if staff is None:
        raise AuthError("not logged in", status_code=401)
    return staff
