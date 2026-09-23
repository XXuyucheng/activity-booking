#!/bin/sh
set -e
alembic upgrade head
# 本机 compose.yaml 设 UVICORN_RELOAD=1。生产 compose.prod.yaml 显式关掉。
if [ "$UVICORN_RELOAD" = "1" ]; then
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
fi
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
