from __future__ import annotations

import re
import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

_PHONE = re.compile(r"^1[3-9]\d{9}$")


class CreateBookingRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schedule_id: uuid.UUID
    contact_name: str = Field(min_length=1, max_length=64)
    contact_phone: str
    adult_count: int = Field(ge=1)
    child_count: int = Field(ge=0)
    remark: str = Field(default="", max_length=512)

    @field_validator("contact_name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        name = value.strip()
        if not name:
            raise ValueError("contact_name required")
        return name

    @field_validator("contact_phone")
    @classmethod
    def valid_phone(cls, value: str) -> str:
        phone = value.strip()
        if not _PHONE.fullmatch(phone):
            raise ValueError("invalid phone")
        return phone

    @field_validator("remark")
    @classmethod
    def strip_remark(cls, value: str) -> str:
        return value.strip()


class BookingResponse(BaseModel):
    """预约详情。不含 openid。"""

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    camp_slug: str
    activity_id: uuid.UUID
    activity_name: str
    schedule_id: uuid.UUID
    start_time: datetime
    end_time: datetime
    contact_name: str
    contact_phone: str
    adult_count: int
    child_count: int
    remark: str
    total_price: Decimal
    unpaid_amount: Decimal
    status: str
    created_at: datetime


class UpdateUnpaidAmountRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    unpaid_amount: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
