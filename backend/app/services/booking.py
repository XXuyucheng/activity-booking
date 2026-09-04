from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ApiError, ConflictError, NotFoundError
from app.models.activity import Activity
from app.models.booking import Booking
from app.models.schedule import Schedule
from app.models.user import User
from app.repositories.activity import ActivityRepository
from app.repositories.booking import BookingRepository
from app.repositories.camp import CampRepository
from app.repositories.schedule import ScheduleRepository
from app.schemas.booking import BookingResponse, CreateBookingRequest
from app.services.camp import PUBLISHED

CANCEL_LEAD = timedelta(hours=24)


def _aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value


class BookingService:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._bookings = BookingRepository(db)
        self._schedules = ScheduleRepository(db)
        self._activities = ActivityRepository(db)
        self._camps = CampRepository(db)

    def create(self, user: User, payload: CreateBookingRequest) -> BookingResponse:
        schedule = self._schedules.get_by_id_for_update(payload.schedule_id)
        activity = self._require_bookable(schedule)
        heads = payload.adult_count + payload.child_count
        remaining = schedule.capacity - schedule.booked_count
        if heads > remaining:
            raise ConflictError("not enough remaining")
        total = (
            activity.price * payload.adult_count
            + activity.child_price * payload.child_count
        )
        booking = Booking(
            id=uuid.uuid4(),
            user_id=user.id,
            camp_id=activity.camp_id,
            activity_id=activity.id,
            schedule_id=schedule.id,
            contact_name=payload.contact_name,
            contact_phone=payload.contact_phone,
            adult_count=payload.adult_count,
            child_count=payload.child_count,
            remark=payload.remark,
            total_price=total,
            status="pending",
        )
        self._schedules.add_booked(schedule, heads)
        try:
            self._bookings.add(booking)
            self._db.commit()
        except IntegrityError as exc:
            self._db.rollback()
            raise ConflictError("not enough remaining") from exc
        return self._to_response(booking, activity, schedule)

    def list_mine(self, user: User) -> list[BookingResponse]:
        bookings = self._bookings.list_by_user_id(user.id)
        return [self._response_for(booking) for booking in bookings]

    def get_mine(self, user: User, booking_id: str) -> BookingResponse:
        booking = self._owned(user, booking_id)
        return self._response_for(booking)

    def cancel(self, user: User, booking_id: str) -> BookingResponse:
        booking = self._owned(user, booking_id)
        if booking.status != "pending":
            raise ApiError("booking cannot be cancelled")
        schedule = self._schedules.get_by_id_for_update(booking.schedule_id)
        if schedule is None:
            raise NotFoundError("schedule not found")
        now = datetime.now(UTC)
        if now + CANCEL_LEAD > _aware(schedule.start_time):
            raise ApiError("too late to cancel")
        heads = booking.adult_count + booking.child_count
        booking.status = "expired"
        self._schedules.add_booked(schedule, -heads)
        self._db.commit()
        activity = self._activities.get_by_id(booking.activity_id)
        if activity is None:
            raise NotFoundError("activity not found")
        return self._to_response(booking, activity, schedule)

    def _owned(self, user: User, booking_id: str) -> Booking:
        try:
            uid = uuid.UUID(booking_id)
        except ValueError as exc:
            raise NotFoundError("booking not found") from exc
        booking = self._bookings.get_by_id(uid)
        if booking is None or booking.user_id != user.id:
            raise NotFoundError("booking not found")
        return booking

    def _require_bookable(self, schedule: Schedule | None) -> Activity:
        if schedule is None:
            raise NotFoundError("schedule not found")
        now = datetime.now(UTC)
        if schedule.status != "open" or _aware(schedule.start_time) <= now:
            raise ConflictError("schedule not available")
        activity = self._activities.get_by_id(schedule.activity_id)
        if activity is None or activity.status != "open":
            raise NotFoundError("activity not found")
        camp = self._camps.get_by_id(activity.camp_id)
        if camp is None or camp.status != PUBLISHED:
            raise NotFoundError("activity not found")
        return activity

    def _response_for(self, booking: Booking) -> BookingResponse:
        activity = self._activities.get_by_id(booking.activity_id)
        schedule = self._schedules.get_by_id(booking.schedule_id)
        if activity is None or schedule is None:
            raise NotFoundError("booking not found")
        return self._to_response(booking, activity, schedule)

    def _to_response(
        self,
        booking: Booking,
        activity: Activity,
        schedule: Schedule,
    ) -> BookingResponse:
        return BookingResponse(
            id=booking.id,
            activity_id=activity.id,
            activity_name=activity.name,
            schedule_id=schedule.id,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            contact_name=booking.contact_name,
            contact_phone=booking.contact_phone,
            adult_count=booking.adult_count,
            child_count=booking.child_count,
            remark=booking.remark,
            total_price=booking.total_price,
            status=booking.status,
            created_at=booking.created_at,
        )
