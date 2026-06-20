#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT:${PYTHONPATH:-}"

exec python3 -m uvicorn apps.api_server:app --host "${PATHVLA_API_HOST:-0.0.0.0}" --port "${PATHVLA_API_PORT:-8000}"
