"""Schema 层：Pydantic Request / Response / Query / Path。不负责数据库操作。"""

from app.schemas.activity import (
    ActivityDetailResponse,
    ActivityListItem,
    AdminActivityItem,
    ScheduleResponse,
    UpdateActivityPricesRequest,
    UpdateScheduleRequest,
)
from app.schemas.auth import MeResponse
from app.schemas.booking import BookingResponse, CreateBookingRequest
from app.schemas.camp import CampResponse
from app.schemas.staff import StaffLoginRequest, StaffMeResponse

__all__ = [
    "ActivityDetailResponse",
    "ActivityListItem",
    "AdminActivityItem",
    "BookingResponse",
    "CampResponse",
    "CreateBookingRequest",
    "MeResponse",
    "ScheduleResponse",
    "StaffLoginRequest",
    "StaffMeResponse",
    "UpdateActivityPricesRequest",
    "UpdateScheduleRequest",
]
