"""员工历史排期查询。不写 SQL。"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff, get_db
from app.models.staff import StaffUser
from app.schemas.activity import HistoryScheduleItem
from app.services.activity import ActivityService

router = APIRouter(prefix="/api/admin/history", tags=["admin-history"])


@router.get("", response_model=list[HistoryScheduleItem])
def list_history(
    db: Session = Depends(get_db),
    staff: StaffUser = Depends(get_current_staff),
) -> list[HistoryScheduleItem]:
    return ActivityService(db).list_history(staff.camp_id)
