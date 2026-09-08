"""扫描未来 24 小时内 pending 预约并写提醒日志。

在 backend 目录执行：后端/bin/python scripts/send_reminders.py
可重复执行（crontab）；同一预约已 sent/skipped 的 reminder 不会再发。
凭据或模板 ID 未配时不请求微信，只写 status=skipped。
"""

from __future__ import annotations

import sys
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from app.core import db as db_mod
from app.services.notification import NotificationService


def main() -> None:
    db_mod.get_engine()
    assert db_mod.SessionLocal is not None
    session = db_mod.SessionLocal()
    try:
        count = NotificationService(session).notify_reminders()
        print(f"reminder logs written: {count}")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
