from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ScheduleResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    start_time: datetime
    end_time: datetime
    capacity: int
    booked_count: int
    remaining: int
    status: str


class ActivityListItem(BaseModel):
    """列表项。status 为按排期推导的 open | full，不是库里的 activities.status。"""

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    name: str
    cover: str
    duration: int | None
    price: Decimal
    child_price: Decimal
    status: Literal["open", "full"]


class ActivityDetailResponse(ActivityListItem):
    description: str
    notice: str
    camp_slug: str
    schedules: list[ScheduleResponse] = Field(default_factory=list)


class AdminScheduleBooking(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    contact_name: str
    contact_phone: str
    adult_count: int
    child_count: int
    status: str
    start_time: datetime
    end_time: datetime
    total_price: Decimal
    unpaid_amount: Decimal


class AdminScheduleItem(ScheduleResponse):
    bookings: list[AdminScheduleBooking] = Field(default_factory=list)
    revenue: Decimal = Field(default=Decimal("0.00"))


class AdminActivityItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    name: str
    duration: int | None
    price: Decimal
    child_price: Decimal
    schedules: list[AdminScheduleItem] = Field(default_factory=list)


class UpdateActivityPricesRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    child_price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)


class UpdateScheduleRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    capacity: int | None = Field(default=None, ge=0)
    status: Literal["open", "closed"] | None = None

    @model_validator(mode="after")
    def require_change(self) -> UpdateScheduleRequest:
        if self.capacity is None and self.status is None:
            raise ValueError("capacity or status required")
        return self
