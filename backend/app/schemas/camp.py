from __future__ import annotations

import uuid

from pydantic import BaseModel, ConfigDict


class CampResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: uuid.UUID
    slug: str
    name: str
    description: str
    status: str
