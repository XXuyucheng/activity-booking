"""中间件：CORS（H5 带 Cookie 调 /api/auth/me）。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings


def register_middleware(app: FastAPI) -> None:
    settings = get_settings()
    origins = list(dict.fromkeys([settings.h5_origin, settings.admin_origin]))
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )
