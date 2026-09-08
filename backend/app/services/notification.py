from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.integrations.wechat.notify import WechatNotifyClient
from app.models.booking import Booking
from app.models.notification import NotificationLog
from app.repositories.activity import ActivityRepository
from app.repositories.booking import BookingRepository
from app.repositories.notification import NotificationRepository
from app.repositories.schedule import ScheduleRepository
from app.repositories.user import UserRepository

logger = logging.getLogger(__name__)

TYPE_SUCCESS = "success"
TYPE_CANCEL = "cancel"
TYPE_REMINDER = "reminder"
STATUS_SKIPPED = "skipped"
STATUS_SENT = "sent"
STATUS_FAILED = "failed"
REMINDER_WINDOW = timedelta(hours=24)
_SH = ZoneInfo("Asia/Shanghai")


def _clip_error(message: str) -> str:
    text = message.strip() or "notify failed"
    return text[:1024]


class NotificationService:
    def __init__(self, db: Session, settings: Settings | None = None) -> None:
        self._db = db
        self._settings = settings or get_settings()
        self._logs = NotificationRepository(db)
        self._bookings = BookingRepository(db)
        self._users = UserRepository(db)
        self._activities = ActivityRepository(db)
        self._schedules = ScheduleRepository(db)
        self._client = WechatNotifyClient(self._settings)

    def notify_created(self, booking_id: uuid.UUID) -> None:
        self._dispatch(booking_id, TYPE_SUCCESS)

    def notify_cancelled(self, booking_id: uuid.UUID) -> None:
        self._dispatch(booking_id, TYPE_CANCEL)

    def notify_reminders(self) -> int:
        now = datetime.now(UTC)
        bookings = self._bookings.list_pending_starting_between(
            now,
            now + REMINDER_WINDOW,
        )
        sent = 0
        for booking in bookings:
            if self._logs.has_terminal(booking.id, TYPE_REMINDER):
                continue
            self._dispatch(booking.id, TYPE_REMINDER)
            sent += 1
        return sent

    def _dispatch(self, booking_id: uuid.UUID, kind: str) -> None:
        booking = self._bookings.get_by_id(booking_id)
        if booking is None:
            logger.warning("notify skipped: booking missing %s", booking_id)
            return
        user = self._users.get_by_id(booking.user_id)
        if user is None:
            self._write_log(booking, kind, STATUS_FAILED, "user not found")
            return
        if not self._settings.wechat_notify_ready(kind):
            self._write_log(booking, kind, STATUS_SKIPPED, None)
            return
        try:
            self._client.send_template(
                openid=user.openid,
                template_id=self._settings.wechat_template_id(kind),
                data=self._template_data(booking),
                url=f"{self._settings.h5_origin.rstrip('/')}/bookings/{booking.id}",
            )
        except Exception as exc:
            logger.warning("wechat template %s failed booking=%s", kind, booking_id)
            self._write_log(booking, kind, STATUS_FAILED, _clip_error(str(exc)))
            return
        self._write_log(booking, kind, STATUS_SENT, None, sent=True)

    def _template_data(self, booking: Booking) -> dict[str, dict[str, str]]:
        activity = self._activities.get_by_id(booking.activity_id)
        schedule = self._schedules.get_by_id(booking.schedule_id)
        name = activity.name if activity is not None else ""
        when = ""
        if schedule is not None:
            start = schedule.start_time
            if start.tzinfo is None:
                start = start.replace(tzinfo=UTC)
            when = start.astimezone(_SH).strftime("%Y-%m-%d %H:%M")
        heads = f"成人{booking.adult_count} 儿童{booking.child_count}"
        price = f"{booking.total_price}"
        return {
            "keyword1": {"value": name},
            "keyword2": {"value": when},
            "keyword3": {"value": heads},
            "keyword4": {"value": price},
        }

    def _write_log(
        self,
        booking: Booking,
        kind: str,
        status: str,
        error_message: str | None,
        sent: bool = False,
    ) -> None:
        log = NotificationLog(
            id=uuid.uuid4(),
            user_id=booking.user_id,
            booking_id=booking.id,
            type=kind,
            status=status,
            sent_at=datetime.now(UTC) if sent else None,
            error_message=error_message,
        )
        self._logs.add(log)
        self._db.commit()
