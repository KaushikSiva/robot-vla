#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT:${PYTHONPATH:-}"

SCENE="${1:-room}"
INSTRUCTION="${2:-Go to the red bin, avoid the chair, inspect the table, then return home.}"
ALLOW_PROXY="${3:-0}"
ALLOW_KINEMATIC="${4:-0}"
ALLOW_RULE_PLANNER="${5:-0}"

if [[ "$ALLOW_RULE_PLANNER" != "1" ]]; then
  [[ -n "${VLA_ENDPOINT:-}" ]] || { echo "VLA_ENDPOINT is required for recorded demo strict mode."; exit 1; }
fi
if [[ "$ALLOW_PROXY" != "1" ]]; then
  [[ -n "${UNITREE_G1_USD_PATH:-}" ]] || { echo "UNITREE_G1_USD_PATH is required unless ALLOW_PROXY=1."; exit 1; }
fi

bash scripts/check_gpu.sh
bash scripts/check_isaac.sh

CMD=(
  python3 -m isaac_ext.pathvla_unitree.tasks.room_nav_env
  --scene "$SCENE"
  --instruction "$INSTRUCTION"
  --robot unitree_g1
  --live none
  --record-video
)

if [[ "$ALLOW_RULE_PLANNER" == "1" ]]; then
  CMD+=(--no-require-vla --allow-rule-planner)
else
  CMD+=(--require-vla)
fi

if [[ "$ALLOW_PROXY" == "1" ]]; then
  CMD+=(--allow-proxy)
fi
if [[ "$ALLOW_KINEMATIC" == "1" ]]; then
  CMD+=(--allow-kinematic-control)
fi

exec "${CMD[@]}"
