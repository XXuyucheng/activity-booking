from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routers import (
    activities,
    admin_activities,
    admin_auth,
    admin_bookings,
    admin_schedules,
    auth,
    bookings,
    camps,
    health,
)
from app.core.db import dispose_engine, get_engine
from app.core.exceptions import register_exception_handlers
from app.core.middleware import register_middleware


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """生命周期：初始化 / 关闭引擎。表结构只通过 Alembic 迁移。"""
    get_engine()
    yield
    dispose_engine()


def create_app() -> FastAPI:
    application = FastAPI(title="activity-booking", lifespan=lifespan)
    register_middleware(application)
    register_exception_handlers(application)
    application.include_router(health.router)
    application.include_router(auth.router)
    application.include_router(admin_auth.router)
    application.include_router(admin_bookings.router)
    application.include_router(admin_activities.router)
    application.include_router(admin_schedules.router)
    application.include_router(camps.router)
    application.include_router(activities.router)
    application.include_router(bookings.router)
    return application


app = create_app()
