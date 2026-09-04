"""幂等写入麓禾村目录数据。在 backend 目录执行：后端/bin/python scripts/seed_catalog.py"""

from __future__ import annotations

import sys
import uuid
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

_BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core import db as db_mod
from app.models.activity import Activity
from app.models.booking import Booking
from app.models.camp import Camp
from app.models.schedule import Schedule

TZ = ZoneInfo("Asia/Shanghai")

LUHE_INTRO = "麓禾村 莫干山麓的心安之地 等你来 慢慢生活"

ACTIVITIES: list[dict] = [
    {
        "name": "挖甘蔗+榨汁+甘蔗棒棒糖",
        "description": (
            "走进甘蔗田亲手砍一节，现场榨汁，再做成一支甘蔗棒棒糖。"
            "适合亲子慢玩，约两小时。"
        ),
        "cover": "activity-cover.png",
        "duration": 120,
        "price": Decimal("68.00"),
        "child_price": Decimal("38.00"),
        "notice": "3–12 岁享儿童价，需家长全程陪同；如遇小雨活动照常，大雨提前通知改期。",
        "kind": "cane",
    },
    {
        "name": "划船捞河蚌+制作珍珠首饰",
        "description": (
            "清晨下河划船捞河蚌，开蚌取珠，把一颗珍珠做成手链或耳坠带回家。"
        ),
        "cover": "activity-cover-pearl.png",
        "duration": 90,
        "price": Decimal("128.00"),
        "child_price": Decimal("88.00"),
        "notice": "3–12 岁享儿童价；水上活动儿童须穿救生衣并由家长同船陪同。",
        "kind": "pearl",
    },
    {
        "name": "挖地瓜+古法烤地瓜",
        "description": "田间挖地瓜，用柴火窑慢慢烤熟。傍晚出窑，热乎乎分着吃。",
        "cover": "kaodigua.webp",
        "duration": 90,
        "price": Decimal("58.00"),
        "child_price": Decimal("28.00"),
        "notice": "3–12 岁享儿童价；窑边温度高，请家长看好小朋友，勿靠近火口。",
        "kind": "yam",
    },
]


def _next_saturday(after: date) -> date:
    day = after + timedelta(days=1)
    while day.weekday() != 5:
        day += timedelta(days=1)
    return day


def _at(day: date, hour: int, minute: int) -> datetime:
    return datetime(day.year, day.month, day.day, hour, minute, tzinfo=TZ)


def _add_slot(
    session: Session,
    activity_id: uuid.UUID,
    start: datetime,
    end: datetime,
    capacity: int,
    booked: int,
) -> None:
    session.add(
        Schedule(
            id=uuid.uuid4(),
            activity_id=activity_id,
            start_time=start,
            end_time=end,
            capacity=capacity,
            booked_count=booked,
            status="open",
        )
    )


def _upsert_camp(
    session: Session,
    slug: str,
    name: str,
    description: str,
    status: str,
) -> Camp:
    camp = session.scalar(select(Camp).where(Camp.slug == slug))
    if camp is None:
        camp = Camp(
            id=uuid.uuid4(),
            slug=slug,
            name=name,
            description=description,
            status=status,
        )
        session.add(camp)
        session.flush()
        return camp
    camp.name = name
    camp.description = description
    camp.status = status
    return camp


def _upsert_activity(session: Session, camp: Camp, spec: dict) -> Activity:
    activity = session.scalar(
        select(Activity).where(
            Activity.camp_id == camp.id,
            Activity.name == spec["name"],
        )
    )
    if activity is None:
        activity = Activity(
            id=uuid.uuid4(),
            camp_id=camp.id,
            name=spec["name"],
            description=spec["description"],
            cover=spec["cover"],
            duration=spec["duration"],
            status="open",
            price=spec["price"],
            child_price=spec["child_price"],
            notice=spec["notice"],
        )
        session.add(activity)
        session.flush()
        return activity
    activity.description = spec["description"]
    activity.cover = spec["cover"]
    activity.duration = spec["duration"]
    activity.status = "open"
    activity.price = spec["price"]
    activity.child_price = spec["child_price"]
    activity.notice = spec["notice"]
    return activity


def _has_bookings(session: Session, activity_id: uuid.UUID) -> bool:
    return (
        session.scalar(
            select(Booking.id).where(Booking.activity_id == activity_id).limit(1)
        )
        is not None
    )


def _replace_schedules(session: Session, activity: Activity, kind: str) -> None:
    session.execute(delete(Schedule).where(Schedule.activity_id == activity.id))
    saturday = _next_saturday(date.today())
    sunday = saturday + timedelta(days=1)
    next_saturday = saturday + timedelta(days=7)
    next_sunday = sunday + timedelta(days=7)
    monday = sunday + timedelta(days=1)
    tuesday = monday + timedelta(days=1)
    next_monday = monday + timedelta(days=7)

    if kind == "cane":
        days = [saturday, sunday, next_saturday, next_sunday]
        times = [(10, 0, 11, 30), (14, 0, 15, 30), (16, 0, 17, 30)]
        for index, day in enumerate(days):
            for slot_i, (sh, sm, eh, em) in enumerate(times):
                booked = 8 if index == 2 else (8 if slot_i == 0 and index == 0 else 3 + slot_i)
                booked = min(booked, 8)
                _add_slot(
                    session,
                    activity.id,
                    _at(day, sh, sm),
                    _at(day, eh, em),
                    8,
                    booked,
                )
        return

    if kind == "pearl":
        days = [monday, tuesday, next_monday]
        times = [(6, 30, 8, 0), (8, 30, 10, 0)]
        for day in days:
            for sh, sm, eh, em in times:
                _add_slot(
                    session,
                    activity.id,
                    _at(day, sh, sm),
                    _at(day, eh, em),
                    8,
                    8,
                )
        return

    days = [tuesday, tuesday + timedelta(days=1), next_monday + timedelta(days=1), next_monday + timedelta(days=2)]
    times = [(15, 0, 16, 30), (17, 0, 18, 30)]
    for index, day in enumerate(days):
        for slot_i, (sh, sm, eh, em) in enumerate(times):
            booked = 10 if index == 2 else (5 + slot_i)
            booked = min(booked, 10)
            _add_slot(
                session,
                activity.id,
                _at(day, sh, sm),
                _at(day, eh, em),
                10,
                booked,
            )


def seed(session: Session) -> None:
    luhe = _upsert_camp(
        session,
        slug="luhe",
        name="麓禾村营地",
        description=LUHE_INTRO,
        status="published",
    )
    _upsert_camp(
        session,
        slug="hidden-draft",
        name="未发布草稿营地",
        description="游客不可见",
        status="draft",
    )
    for spec in ACTIVITIES:
        activity = _upsert_activity(session, luhe, spec)
        if _has_bookings(session, activity.id):
            continue
        _replace_schedules(session, activity, spec["kind"])
    session.commit()


def main() -> None:
    db_mod.get_engine()
    assert db_mod.SessionLocal is not None
    session = db_mod.SessionLocal()
    try:
        seed(session)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
    print("seeded camp slug=luhe (published) and hidden-draft (draft)")


if __name__ == "__main__":
    main()
