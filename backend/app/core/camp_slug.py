"""营地 slug 校验。用于 URL 与 OAuth state。"""

from __future__ import annotations

import re

DEFAULT_CAMP_SLUG = "luhe"
CAMP_SLUG_RE = re.compile(r"^[a-z0-9-]{1,64}$")


def parse_camp_slug(value: str | None) -> str | None:
    slug = (value or "").strip().lower()
    if not CAMP_SLUG_RE.fullmatch(slug):
        return None
    return slug
