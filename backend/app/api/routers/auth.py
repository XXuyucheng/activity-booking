"""微信登录：start / callback / me / logout。不写 SQL、不调微信 HTTP。"""

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_session_id
from app.core.config import get_settings
from app.schemas.auth import MeResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _set_session_cookie(response: Response, session_id: str) -> None:
    settings = get_settings()
    response.set_cookie(
        key=settings.session_cookie_name,
        value=session_id,
        max_age=settings.session_ttl_seconds,
        httponly=True,
        samesite="lax",
        path="/",
        secure=settings.session_cookie_secure,
    )


def _clear_session_cookie(response: Response) -> None:
    settings = get_settings()
    response.delete_cookie(
        key=settings.session_cookie_name,
        path="/",
        samesite="lax",
        secure=settings.session_cookie_secure,
        httponly=True,
    )


@router.get("/wechat/start")
def wechat_start(db: Session = Depends(get_db)) -> RedirectResponse:
    location = AuthService(db).start_url()
    return RedirectResponse(url=location, status_code=302)


@router.get("/wechat/callback")
def wechat_callback(
    request: Request,
    db: Session = Depends(get_db),
) -> RedirectResponse:
    result = AuthService(db).complete_login(
        request.query_params.get("code"),
        request.query_params.get("state"),
    )
    response = RedirectResponse(url=get_settings().h5_origin, status_code=302)
    _set_session_cookie(response, result.session.id)
    return response


@router.get("/me", response_model=MeResponse)
def me(
    db: Session = Depends(get_db),
    session_id: str | None = Depends(get_session_id),
) -> MeResponse:
    user = AuthService(db).current_user(session_id)
    if user is None:
        return MeResponse(id=None, logged_in=False)
    return MeResponse(id=user.id, logged_in=True)


@router.post("/logout", status_code=204)
def logout(
    response: Response,
    db: Session = Depends(get_db),
    session_id: str | None = Depends(get_session_id),
) -> None:
    AuthService(db).logout(session_id)
    _clear_session_cookie(response)
