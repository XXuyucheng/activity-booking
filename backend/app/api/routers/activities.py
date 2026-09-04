"""活动只读：详情 + 排期库存。不写 SQL。"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.activity import ActivityDetailResponse
from app.services.activity import ActivityService

router = APIRouter(prefix="/api/activities", tags=["activities"])


@router.get("/{activity_id}", response_model=ActivityDetailResponse)
def get_activity(
    activity_id: str,
    db: Session = Depends(get_db),
) -> ActivityDetailResponse:
    return ActivityService(db).get_detail(activity_id)
