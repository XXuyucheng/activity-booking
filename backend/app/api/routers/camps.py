"""营地只读：介绍与活动列表。不写 SQL。"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.activity import ActivityListItem
from app.schemas.camp import CampResponse
from app.services.activity import ActivityService
from app.services.camp import CampService

router = APIRouter(prefix="/api/camps", tags=["camps"])


@router.get("/{slug}", response_model=CampResponse)
def get_camp(slug: str, db: Session = Depends(get_db)) -> CampResponse:
    camp = CampService(db).get_published_by_slug(slug)
    return CampResponse.model_validate(camp)


@router.get("/{slug}/activities", response_model=list[ActivityListItem])
def list_camp_activities(
    slug: str,
    db: Session = Depends(get_db),
) -> list[ActivityListItem]:
    return ActivityService(db).list_for_camp_slug(slug)
