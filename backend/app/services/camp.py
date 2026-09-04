from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.camp import Camp
from app.repositories.camp import CampRepository

PUBLISHED = "published"


class CampService:
    def __init__(self, db: Session) -> None:
        self._repo = CampRepository(db)

    def get_published_by_slug(self, slug: str) -> Camp:
        camp = self._repo.get_by_slug(slug)
        if camp is None or camp.status != PUBLISHED:
            raise NotFoundError("camp not found")
        return camp
