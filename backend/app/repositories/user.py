from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_openid(self, openid: str) -> User | None:
        return self._db.scalar(select(User).where(User.openid == openid))

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self._db.get(User, user_id)

    def add(self, user: User) -> User:
        self._db.add(user)
        self._db.flush()
        return user
