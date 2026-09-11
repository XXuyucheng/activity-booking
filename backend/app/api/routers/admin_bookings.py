"""员工预约列表与建联。不写 SQL、不调微信。"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_staff, get_db
from app.models.staff import StaffUser
from app.schemas.booking import BookingResponse, UpdateUnpaidAmountRequest
from app.services.booking import BookingService

router = APIRouter(prefix="/api/admin/bookings", tags=["admin-bookings"])


@router.get("", response_model=list[BookingResponse])
def list_bookings(
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
    staff: StaffUser = Depends(get_current_staff),
) -> list[BookingResponse]:
    return BookingService(db).list_for_camp(staff.camp_id, status)


@router.post("/{booking_id}/contact", response_model=BookingResponse)
def contact_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    staff: StaffUser = Depends(get_current_staff),
) -> BookingResponse:
    return BookingService(db).mark_contacted(staff.camp_id, booking_id)


@router.post("/{booking_id}/unpaid", response_model=BookingResponse)
def update_unpaid_amount(
    booking_id: str,
    payload: UpdateUnpaidAmountRequest,
    db: Session = Depends(get_db),
    staff: StaffUser = Depends(get_current_staff),
) -> BookingResponse:
    return BookingService(db).update_unpaid(staff.camp_id, booking_id, payload)


@router.post("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    staff: StaffUser = Depends(get_current_staff),
) -> BookingResponse:
    return BookingService(db).cancel_for_camp(staff.camp_id, booking_id)
