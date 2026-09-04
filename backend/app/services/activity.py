from __future__ import annotations

import uuid
from typing import Literal

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.activity import Activity
from app.models.schedule import Schedule
from app.repositories.activity import ActivityRepository
from app.repositories.camp import CampRepository
from app.repositories.schedule import ScheduleRepository
from app.schemas.activity import (
    ActivityDetailResponse,
    ActivityListItem,
    ScheduleResponse,
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


class ActivityService:
    def __init__(self, db: Session) -> None:
        self._camps = CampRepository(db)
        self._activities = ActivityRepository(db)
        self._schedules = ScheduleRepository(db)
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
            schedules=[_schedule_response(schedule) for schedule in schedules],
        )

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
