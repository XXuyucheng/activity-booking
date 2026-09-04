from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


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
    schedules: list[ScheduleResponse] = Field(default_factory=list)
