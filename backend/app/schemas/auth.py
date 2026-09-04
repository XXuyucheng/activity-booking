from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict, Field


class MeResponse(BaseModel):
    """登录态。不含 openid。"""

    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID | None = Field(default=None)
    logged_in: bool
