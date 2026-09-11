#!/bin/sh
set -e
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root/frontend"
npm ci
npm run build
cd "$root/admin"
npm ci
npm run build
