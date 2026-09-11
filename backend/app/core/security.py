"""HMAC state、随机 session id、员工密码哈希。"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import time

import bcrypt

from app.core.camp_slug import parse_camp_slug

_STATE_MAX_AGE = 10 * 60
_DUMMY_HASH = bcrypt.hashpw(b"dummy-password", bcrypt.gensalt())


def new_session_id() -> str:
    return secrets.token_urlsafe(32)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


def verify_password(password: str, password_hash: str | None) -> bool:
    digest = password_hash.encode("utf-8") if password_hash else _DUMMY_HASH
    try:
        return bcrypt.checkpw(password.encode("utf-8"), digest)
    except ValueError:
        return False


def sign_oauth_state(secret: str, camp_slug: str) -> str:
    slug = parse_camp_slug(camp_slug)
    if slug is None:
        raise ValueError("invalid camp slug")
    nonce = secrets.token_urlsafe(16)
    issued = str(int(time.time()))
    payload = f"{issued}.{nonce}.{slug}"
    digest = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{digest}"


def verify_oauth_state(secret: str, state: str) -> str | None:
    parts = state.split(".")
    if len(parts) != 4:
        return None
    issued, nonce, camp_slug, digest = parts
    if parse_camp_slug(camp_slug) is None:
        return None
    payload = f"{issued}.{nonce}.{camp_slug}"
    expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, expected):
        return None
    try:
        age = time.time() - int(issued)
    except ValueError:
        return None
    if not 0 <= age <= _STATE_MAX_AGE:
        return None
    return camp_slug
