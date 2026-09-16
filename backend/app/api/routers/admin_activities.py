"""员工活动改价。不写 SQL。"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff, get_db
from app.models.staff import StaffUser
from app.schemas.activity import (
    AdminActivityItem,
    CreateScheduleRequest,
    UpdateActivityPricesRequest,
)
from app.services.activity import ActivityService

router = APIRouter(prefix="/api/admin/activities", tags=["admin-activities"])


@router.get("", response_model=list[AdminActivityItem])
def list_activities(
    db: Session = Depends(get_db),
    staff: StaffUser = Depends(get_current_staff),
) -> list[AdminActivityItem]:
    return ActivityService(db).list_for_camp_admin(staff.camp_id)


@router.post("/{activity_id}", response_model=AdminActivityItem)
def update_activity_prices(
    activity_id: str,
    payload: UpdateActivityPricesRequest,
    db: Session = Depends(get_db),
    staff: StaffUser = Depends(get_current_staff),
) -> AdminActivityItem:
    return ActivityService(db).update_prices(staff.camp_id, activity_id, payload)


@router.post("/{activity_id}/schedules", response_model=AdminActivityItem)
def create_schedule(
    activity_id: str,
    payload: CreateScheduleRequest,
    db: Session = Depends(get_db),
    staff: StaffUser = Depends(get_current_staff),
) -> AdminActivityItem:
    return ActivityService(db).create_schedule(staff.camp_id, activity_id, payload)
