from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StaffLoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)

    @field_validator("username")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        return value.strip().lower()


class StaffMeResponse(BaseModel):
    """员工登录态。不含密码哈希。"""

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    username: str
    camp_id: uuid.UUID
    camp_slug: str
    camp_name: str
