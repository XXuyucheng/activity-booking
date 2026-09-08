"""微信模板消息 Client。不创建 User、不写 Booking。"""

from __future__ import annotations

import time
from dataclasses import dataclass

import httpx

from app.core.config import Settings, get_settings

_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
_SEND_URL = "https://api.weixin.qq.com/cgi-bin/message/template/send"


@dataclass
class _CachedToken:
    value: str
    expires_at: float


class WechatNotifyClient:
    """client_credential token + 模板发送。仅在凭据与模板 ID 已配时由 Service 调用。"""

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or get_settings()
        self._token: _CachedToken | None = None

    def send_template(
        self,
        openid: str,
        template_id: str,
        data: dict[str, dict[str, str]],
        url: str,
    ) -> None:
        token = self.get_access_token()
        with httpx.Client(timeout=10.0) as client:
            response = client.post(
                _SEND_URL,
                params={"access_token": token},
                json={
                    "touser": openid,
                    "template_id": template_id,
                    "url": url,
                    "data": data,
                },
            )
            response.raise_for_status()
            body = response.json()
        errcode = body.get("errcode") or 0
        if errcode:
            raise RuntimeError(str(body.get("errmsg") or "template send failed"))

    def get_access_token(self) -> str:
        now = time.time()
        if self._token is not None and self._token.expires_at > now + 60:
            return self._token.value
        s = self._settings
        with httpx.Client(timeout=10.0) as client:
            response = client.get(
                _TOKEN_URL,
                params={
                    "grant_type": "client_credential",
                    "appid": s.wechat_app_id,
                    "secret": s.wechat_app_secret,
                },
            )
            response.raise_for_status()
            body = response.json()
        if body.get("errcode"):
            raise RuntimeError(str(body.get("errmsg") or "access_token failed"))
        token = body.get("access_token")
        expires_in = int(body.get("expires_in") or 7200)
        if not token:
            raise RuntimeError("access_token missing")
        self._token = _CachedToken(value=str(token), expires_at=now + expires_in)
        return self._token.value
