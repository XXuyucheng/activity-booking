from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.camp import Camp


class CampRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, camp_id: uuid.UUID) -> Camp | None:
        return self._db.get(Camp, camp_id)

    def get_by_slug(self, slug: str) -> Camp | None:
        return self._db.scalar(select(Camp).where(Camp.slug == slug))
