from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, db: Session) -> None:
        self._repo = UserRepository(db)

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self._repo.get_by_id(user_id)

    def get_or_create_by_openid(self, openid: str) -> User:
        user = self._repo.get_by_openid(openid)
        if user is not None:
            return user
        return self._repo.add(User(id=uuid.uuid4(), openid=openid))
