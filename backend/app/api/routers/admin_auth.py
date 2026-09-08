"""员工账号密码登录。不写 SQL、不走微信。"""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff, get_db, get_staff_session_id
from app.core.config import get_settings
from app.models.staff import StaffUser
from app.schemas.staff import StaffLoginRequest, StaffMeResponse
from app.services.staff_auth import StaffAuthService

router = APIRouter(prefix="/api/admin", tags=["admin-auth"])


def _set_admin_cookie(response: Response, session_id: str) -> None:
    settings = get_settings()
    response.set_cookie(
        key=settings.admin_session_cookie_name,
        value=session_id,
        max_age=settings.session_ttl_seconds,
        httponly=True,
        samesite="lax",
        path="/",
        secure=settings.session_cookie_secure,
    )


def _clear_admin_cookie(response: Response) -> None:
    settings = get_settings()
    response.delete_cookie(
        key=settings.admin_session_cookie_name,
        path="/",
        samesite="lax",
        secure=settings.session_cookie_secure,
        httponly=True,
    )


@router.post("/login", response_model=StaffMeResponse)
def login(
    payload: StaffLoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> StaffMeResponse:
    service = StaffAuthService(db)
    result = service.login(payload.username, payload.password)
    _set_admin_cookie(response, result.session.id)
    return service.me_response(result.staff)


@router.post("/logout", status_code=204)
def logout(
    response: Response,
    db: Session = Depends(get_db),
    session_id: str | None = Depends(get_staff_session_id),
) -> None:
    StaffAuthService(db).logout(session_id)
    _clear_admin_cookie(response)


@router.get("/me", response_model=StaffMeResponse)
def me(
    db: Session = Depends(get_db),
    staff: StaffUser = Depends(get_current_staff),
) -> StaffMeResponse:
    return StaffAuthService(db).me_response(staff)
