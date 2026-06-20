#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export PYTHONPATH="$ROOT:${PYTHONPATH:-}"

python3 - <<'PY'
from isaac_ext.pathvla_unitree.tasks.room_nav_env import launch_simulation_app, resolve_simulation_app_class

print("[isaac] Resolving SimulationApp")
simulation_app_cls = resolve_simulation_app_class()
print(f"[isaac] SimulationApp class: {simulation_app_cls}")

print("[isaac] Launching headless Isaac app")
app = launch_simulation_app(headless=True)

try:
    import omni.kit.app
    version = omni.kit.app.get_app().get_build_version()
    print(f"[isaac] Kit build version: {version}")
except Exception as exc:  # noqa: BLE001
    print(f"[isaac] Could not read Kit version: {exc}")

app.update()
app.update()
app.close()
print("[isaac] Isaac runtime checks passed")
PY
