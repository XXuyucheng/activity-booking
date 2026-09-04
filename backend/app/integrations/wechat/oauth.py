from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlencode

import httpx

from app.core.config import Settings, get_settings
from app.core.exceptions import AuthError

MOCK_OPENID = "mock-local-openid"
MOCK_CODE = "mock"
_TOKEN_URL = "https://api.weixin.qq.com/sns/oauth2/access_token"
_AUTHORIZE_URL = "https://open.weixin.qq.com/connect/oauth2/authorize"


@dataclass(frozen=True)
class OAuthToken:
    openid: str
    is_snapshotuser: bool


class WechatOAuthClient:
    """拼授权 URL、用 code 换 openid。不创建 User、不写 Session。"""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()

    def build_authorize_url(self, state: str) -> str:
        s = self._settings
        if not s.wechat_oauth_redirect_uri:
            raise AuthError("WECHAT_OAUTH_REDIRECT_URI is required for real OAuth")
        query = urlencode(
            {
                "appid": s.wechat_app_id,
                "redirect_uri": s.wechat_oauth_redirect_uri,
                "response_type": "code",
                "scope": "snsapi_base",
                "state": state,
            }
        )
        return f"{_AUTHORIZE_URL}?{query}#wechat_redirect"

    def exchange_code(self, code: str) -> OAuthToken:
        if self._settings.wechat_oauth_mock:
            if code != MOCK_CODE:
                raise AuthError("invalid mock code")
            return OAuthToken(openid=MOCK_OPENID, is_snapshotuser=False)

        s = self._settings
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(
                    _TOKEN_URL,
                    params={
                        "appid": s.wechat_app_id,
                        "secret": s.wechat_app_secret,
                        "code": code,
                        "grant_type": "authorization_code",
                    },
                )
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as exc:
            raise AuthError("wechat oauth request failed") from exc
        if data.get("errcode"):
            raise AuthError(data.get("errmsg", "wechat oauth failed"))
        openid = data.get("openid")
        if not openid:
            raise AuthError("wechat oauth missing openid")
        return OAuthToken(
            openid=str(openid),
            is_snapshotuser=data.get("is_snapshotuser") == 1,
        )
