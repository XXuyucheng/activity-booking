from __future__ import annotations

import uuid
from collections import defaultdict
from decimal import Decimal
from typing import Literal

from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models.activity import Activity
from app.models.schedule import Schedule
from app.repositories.activity import ActivityRepository
from app.repositories.booking import BookingRepository
from app.repositories.camp import CampRepository
from app.repositories.schedule import ScheduleRepository
from app.schemas.activity import (
    ActivityDetailResponse,
    ActivityListItem,
    AdminActivityItem,
    AdminScheduleBooking,
    AdminScheduleItem,
    ScheduleResponse,
    UpdateActivityPricesRequest,
    UpdateScheduleRequest,
)
from app.services.camp import PUBLISHED, CampService


def _remaining(schedule: Schedule) -> int:
    return schedule.capacity - schedule.booked_count


def derived_list_status(schedules: list[Schedule]) -> Literal["open", "full"]:
    if not schedules:
        return "open"
    if all(schedule.booked_count >= schedule.capacity for schedule in schedules):
        return "full"
    return "open"


def _schedule_response(schedule: Schedule) -> ScheduleResponse:
    return ScheduleResponse(
        id=schedule.id,
        start_time=schedule.start_time,
        end_time=schedule.end_time,
        capacity=schedule.capacity,
        booked_count=schedule.booked_count,
        remaining=_remaining(schedule),
        status=schedule.status,
    )


def _admin_schedule_item(schedule: Schedule, bookings: list) -> AdminScheduleItem:
    rows = [
        AdminScheduleBooking(
            id=booking.id,
            contact_name=booking.contact_name,
            contact_phone=booking.contact_phone,
            adult_count=booking.adult_count,
            child_count=booking.child_count,
            status=booking.status,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            total_price=booking.total_price,
            unpaid_amount=booking.unpaid_amount,
        )
        for booking in bookings
    ]
    revenue = sum((row.total_price for row in rows), Decimal("0.00"))
    return AdminScheduleItem(
        **_schedule_response(schedule).model_dump(),
        bookings=rows,
        revenue=revenue,
    )


class ActivityService:
    def __init__(self, db: Session) -> None:
        self._db = db
        self._camps = CampRepository(db)
        self._activities = ActivityRepository(db)
        self._schedules = ScheduleRepository(db)
        self._bookings = BookingRepository(db)
        self._camp_service = CampService(db)

    def list_for_camp_slug(self, slug: str) -> list[ActivityListItem]:
        camp = self._camp_service.get_published_by_slug(slug)
        activities = self._activities.list_open_by_camp_id(camp.id)
        return [self._to_list_item(activity) for activity in activities]

    def get_detail(self, activity_id: str) -> ActivityDetailResponse:
        try:
            uid = uuid.UUID(activity_id)
        except ValueError as exc:
            raise NotFoundError("activity not found") from exc
        activity = self._activities.get_by_id(uid)
        if activity is None or activity.status != "open":
            raise NotFoundError("activity not found")
        camp = self._camps.get_by_id(activity.camp_id)
        if camp is None or camp.status != PUBLISHED:
            raise NotFoundError("activity not found")
        schedules = self._schedules.list_open_by_activity_id(activity.id)
        item = self._to_list_item(activity, schedules)
        return ActivityDetailResponse(
            id=item.id,
            name=item.name,
            cover=item.cover,
            duration=item.duration,
            price=item.price,
            child_price=item.child_price,
            status=item.status,
            description=activity.description,
            notice=activity.notice,
            camp_slug=camp.slug,
            schedules=[_schedule_response(schedule) for schedule in schedules],
        )

    def list_for_camp_admin(self, camp_id: uuid.UUID) -> list[AdminActivityItem]:
        activities = self._activities.list_by_camp_id(camp_id)
        items: list[AdminActivityItem] = []
        for activity in activities:
            schedules = self._schedules.list_by_activity_id(activity.id)
            booked = self._bookings.list_active_by_schedule_ids(
                [schedule.id for schedule in schedules],
            )
            by_slot: dict[uuid.UUID, list] = defaultdict(list)
            for booking in booked:
                by_slot[booking.schedule_id].append(booking)
            items.append(
                AdminActivityItem(
                    id=activity.id,
                    name=activity.name,
                    duration=activity.duration,
                    price=activity.price,
                    child_price=activity.child_price,
                    schedules=[
                        _admin_schedule_item(schedule, by_slot[schedule.id])
                        for schedule in schedules
                    ],
                )
            )
        return items

    def update_prices(
        self,
        camp_id: uuid.UUID,
        activity_id: str,
        payload: UpdateActivityPricesRequest,
    ) -> AdminActivityItem:
        activity = self._activity_in_camp(camp_id, activity_id)
        activity.price = payload.price
        activity.child_price = payload.child_price
        self._db.commit()
        return self._admin_item(activity)

    def update_schedule(
        self,
        camp_id: uuid.UUID,
        schedule_id: str,
        payload: UpdateScheduleRequest,
    ) -> AdminActivityItem:
        try:
            uid = uuid.UUID(schedule_id)
        except ValueError as exc:
            raise NotFoundError("schedule not found") from exc
        schedule = self._schedules.get_by_id_for_update(uid)
        if schedule is None:
            raise NotFoundError("schedule not found")
        activity = self._activities.get_by_id(schedule.activity_id)
        if activity is None or activity.camp_id != camp_id:
            raise NotFoundError("schedule not found")
        if payload.capacity is not None:
            if payload.capacity < schedule.booked_count:
                raise ConflictError("capacity below booked_count")
            schedule.capacity = payload.capacity
        if payload.status is not None:
            schedule.status = payload.status
        self._db.commit()
        return self._admin_item(activity)

    def _activity_in_camp(self, camp_id: uuid.UUID, activity_id: str) -> Activity:
        try:
            uid = uuid.UUID(activity_id)
        except ValueError as exc:
            raise NotFoundError("activity not found") from exc
        activity = self._activities.get_by_id(uid)
        if activity is None or activity.camp_id != camp_id:
            raise NotFoundError("activity not found")
        return activity

    def _admin_item(self, activity: Activity) -> AdminActivityItem:
        for item in self.list_for_camp_admin(activity.camp_id):
            if item.id == activity.id:
                return item
        raise NotFoundError("activity not found")

    def _to_list_item(
        self,
        activity: Activity,
        schedules: list[Schedule] | None = None,
    ) -> ActivityListItem:
        if schedules is None:
            schedules = self._schedules.list_open_by_activity_id(activity.id)
        return ActivityListItem(
            id=activity.id,
            name=activity.name,
            cover=activity.cover,
            duration=activity.duration,
            price=activity.price,
            child_price=activity.child_price,
            status=derived_list_status(schedules),
        )
