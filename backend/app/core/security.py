"""HMAC state 与随机 session id。"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import time

_STATE_MAX_AGE = 10 * 60


def new_session_id() -> str:
    return secrets.token_urlsafe(32)


def sign_oauth_state(secret: str) -> str:
    nonce = secrets.token_urlsafe(16)
    issued = str(int(time.time()))
    payload = f"{issued}.{nonce}"
    digest = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{digest}"


def verify_oauth_state(secret: str, state: str) -> bool:
    parts = state.split(".")
    if len(parts) != 3:
        return False
    issued, nonce, digest = parts
    payload = f"{issued}.{nonce}"
    expected = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, expected):
        return False
    try:
        age = time.time() - int(issued)
    except ValueError:
        return False
    return 0 <= age <= _STATE_MAX_AGE
