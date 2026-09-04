"""Schema 层：Pydantic Request / Response / Query / Path。不负责数据库操作。"""

from app.schemas.activity import (
    ActivityDetailResponse,
    ActivityListItem,
    ScheduleResponse,
)
from app.schemas.auth import MeResponse
from app.schemas.booking import BookingResponse, CreateBookingRequest
from app.schemas.camp import CampResponse

__all__ = [
    "ActivityDetailResponse",
    "ActivityListItem",
    "BookingResponse",
    "CampResponse",
    "CreateBookingRequest",
    "MeResponse",
    "ScheduleResponse",
]
