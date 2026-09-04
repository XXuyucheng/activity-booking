"""预约：创建、我的预约、取消。不写 SQL、不调微信。"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.booking import BookingResponse, CreateBookingRequest
from app.services.booking import BookingService

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


@router.post("", response_model=BookingResponse)
def create_booking(
    payload: CreateBookingRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BookingResponse:
    return BookingService(db).create(user, payload)


@router.get("", response_model=list[BookingResponse])
def list_bookings(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[BookingResponse]:
    return BookingService(db).list_mine(user)


@router.get("/{booking_id}", response_model=BookingResponse)
def get_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BookingResponse:
    return BookingService(db).get_mine(user, booking_id)


@router.post("/{booking_id}/cancel", response_model=BookingResponse)
def cancel_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BookingResponse:
    return BookingService(db).cancel(user, booking_id)
