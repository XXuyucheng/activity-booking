"""员工排期改名额 / 开关场次。不写 SQL。"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff, get_db
from app.models.staff import StaffUser
from app.schemas.activity import AdminActivityItem, UpdateScheduleRequest
from app.services.activity import ActivityService

router = APIRouter(prefix="/api/admin/schedules", tags=["admin-schedules"])


@router.post("/{schedule_id}", response_model=AdminActivityItem)
def update_schedule(
    schedule_id: str,
    payload: UpdateScheduleRequest,
    db: Session = Depends(get_db),
    staff: StaffUser = Depends(get_current_staff),
) -> AdminActivityItem:
    return ActivityService(db).update_schedule(staff.camp_id, schedule_id, payload)
