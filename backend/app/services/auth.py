from __future__ import annotations

import logging
from dataclasses import dataclass
from urllib.parse import urlencode

from sqlalchemy.orm import Session

from app.core.camp_slug import DEFAULT_CAMP_SLUG, parse_camp_slug
from app.core.config import DEV_STATE_SECRET, Settings, get_settings
from app.core.exceptions import AuthError, NotFoundError
from app.core.security import sign_oauth_state, verify_oauth_state
from app.integrations.wechat.oauth import MOCK_CODE, WechatOAuthClient
from app.models.session import Session as AuthSession
from app.models.user import User
from app.services.camp import CampService
from app.services.session import SessionService
from app.services.user import UserService

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoginResult:
    session: AuthSession
    user: User
    camp_slug: str


class AuthService:
    def __init__(self, db: Session, settings: Settings | None = None) -> None:
        self._db = db
        self._settings = settings or get_settings()
        self._oauth = WechatOAuthClient(self._settings)
        self._users = UserService(db)
        self._sessions = SessionService(db, self._settings)
        self._camps = CampService(db)

    def start_url(self, camp_slug: str | None) -> str:
        if camp_slug is None or not str(camp_slug).strip():
            slug = DEFAULT_CAMP_SLUG
        else:
            slug = parse_camp_slug(camp_slug)
            if slug is None:
                raise NotFoundError("camp not found")
        self._camps.get_published_by_slug(slug)
        state = sign_oauth_state(self._settings.wechat_oauth_state_secret, slug)
        if self._settings.wechat_oauth_mock:
            logger.warning("WeChat OAuth mock: WECHAT_APP_ID/SECRET empty")
            query = urlencode({"code": MOCK_CODE, "state": state})
            return f"/api/auth/wechat/callback?{query}"
        if self._settings.wechat_oauth_state_secret == DEV_STATE_SECRET:
            raise AuthError("WECHAT_OAUTH_STATE_SECRET is required for real OAuth")
        return self._oauth.build_authorize_url(state)

    def complete_login(self, code: str | None, state: str | None) -> LoginResult:
        if not code or not state:
            raise AuthError("missing code or state")
        camp_slug = verify_oauth_state(self._settings.wechat_oauth_state_secret, state)
        if camp_slug is None:
            raise AuthError("invalid oauth state")
        try:
            self._camps.get_published_by_slug(camp_slug)
        except NotFoundError as exc:
            raise AuthError("invalid oauth state") from exc
        token = self._oauth.exchange_code(code)
        if token.is_snapshotuser:
            raise AuthError("snapshot user is not allowed", status_code=403)
        user = self._users.get_or_create_by_openid(token.openid)
        session = self._sessions.issue(user.id)
        self._db.commit()
        return LoginResult(session=session, user=user, camp_slug=camp_slug)

    def logout(self, session_id: str | None) -> None:
        self._sessions.revoke(session_id)
        self._db.commit()

    def current_user(self, session_id: str | None) -> User | None:
        session = self._sessions.get_valid(session_id)
        if session is None:
            self._db.commit()
            return None
        return self._users.get_by_id(session.user_id)
