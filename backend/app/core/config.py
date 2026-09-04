"""运行配置。微信 Secret 只从环境读取，缺省走 mock。"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(_REPO_ROOT / ".env")

DEV_STATE_SECRET = "dev-only-oauth-state-secret"
_DEFAULT_TTL = 7 * 24 * 60 * 60


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


@dataclass(frozen=True)
class Settings:
    wechat_app_id: str
    wechat_app_secret: str
    wechat_oauth_redirect_uri: str
    wechat_oauth_state_secret: str
    session_cookie_name: str
    session_cookie_secure: bool
    session_ttl_seconds: int
    h5_origin: str

    @property
    def wechat_oauth_mock(self) -> bool:
        return not (self.wechat_app_id and self.wechat_app_secret)


@lru_cache
def get_settings() -> Settings:
    state_secret = _env("WECHAT_OAUTH_STATE_SECRET")
    if not state_secret:
        logging.getLogger(__name__).warning(
            "WECHAT_OAUTH_STATE_SECRET unset; using local dev secret (mock only)",
        )
        state_secret = DEV_STATE_SECRET
    ttl_raw = _env("SESSION_TTL_SECONDS")
    ttl = int(ttl_raw) if ttl_raw else _DEFAULT_TTL
    secure = _env("SESSION_COOKIE_SECURE", "false").lower() in {"1", "true", "yes"}
    return Settings(
        wechat_app_id=_env("WECHAT_APP_ID"),
        wechat_app_secret=_env("WECHAT_APP_SECRET"),
        wechat_oauth_redirect_uri=_env("WECHAT_OAUTH_REDIRECT_URI"),
        wechat_oauth_state_secret=state_secret,
        session_cookie_name=_env("SESSION_COOKIE_NAME") or "ab_session",
        session_cookie_secure=secure,
        session_ttl_seconds=ttl,
        h5_origin=_env("H5_ORIGIN") or "http://127.0.0.1:5173",
    )


@lru_cache
def database_url() -> str:
    url = _env("DATABASE_URL")
    if url:
        return url
    user = _env("POSTGRES_USER") or "booking"
    password = _env("POSTGRES_PASSWORD")
    host_port = _env("POSTGRES_HOST_PORT") or "5433"
    db = _env("POSTGRES_DB") or "activity_booking"
    if not password:
        raise RuntimeError("Set DATABASE_URL or POSTGRES_PASSWORD in .env")
    return f"postgresql+psycopg://{user}:{password}@127.0.0.1:{host_port}/{db}"
