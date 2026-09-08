"""幂等写入麓禾村员工账号。缺 ADMIN_PASSWORD 则退出。"""

from __future__ import annotations

import os
import sys
import uuid
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from sqlalchemy.orm import Session

from app.core import db as db_mod
from app.core.security import hash_password
from app.models.staff import StaffUser
from app.repositories.camp import CampRepository
from app.repositories.staff import StaffUserRepository

CAMP_SLUG = "luhe"


def _env(name: str) -> str:
    return os.environ.get(name, "").strip()


def seed(session: Session) -> StaffUser:
    username = _env("ADMIN_USERNAME").lower()
    password = _env("ADMIN_PASSWORD")
    if not username:
        raise SystemExit("Set ADMIN_USERNAME in .env")
    if not password:
        raise SystemExit("Set ADMIN_PASSWORD in .env")
    if len(password) < 8:
        raise SystemExit("ADMIN_PASSWORD must be at least 8 characters")

    camp = CampRepository(session).get_by_slug(CAMP_SLUG)
    if camp is None or camp.status != "published":
        raise SystemExit("published camp slug=luhe not found; run seed_catalog.py first")

    repo = StaffUserRepository(session)
    staff = repo.get_by_username(username)
    hashed = hash_password(password)
    if staff is None:
        staff = StaffUser(
            id=uuid.uuid4(),
            username=username,
            password_hash=hashed,
            camp_id=camp.id,
            is_active=True,
        )
        repo.add(staff)
    else:
        staff.password_hash = hashed
        staff.camp_id = camp.id
        staff.is_active = True
    session.commit()
    return staff


def main() -> None:
    db_mod.get_engine()
    assert db_mod.SessionLocal is not None
    session = db_mod.SessionLocal()
    try:
        staff = seed(session)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    print(f"seeded staff username={staff.username} camp={CAMP_SLUG}")


if __name__ == "__main__":
    main()
