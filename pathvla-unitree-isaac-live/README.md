# PathVLA Unitree Isaac Live

Real Isaac Lab / Isaac Sim Unitree path simulation with VLA planning and live remote viewing.

## What This Is

This project runs a real Isaac Sim or Isaac Lab scene on a Linux NVIDIA GPU VM such as Brev, calls a real configured VLA endpoint to turn natural-language instructions into structured subgoals, plans waypoints in the live Isaac world, executes movement in simulation, and exposes API/dashboard surfaces for launch, live viewing, and replay.

Target example:

```text
Go to the red bin, avoid the chair, inspect the table, then return home.
```

## What This Is Not

- Not a toy local simulator
- Not a 2D fallback simulator
- Not a fake local Mac mode
- Not silent substitution when assets or endpoints are missing
- Not full humanoid locomotion training
- Not real robot control
- Not mocked VLA by default

## Strict Runtime Behavior

The default path is intentionally strict.

- Missing `VLA_ENDPOINT` fails
- Missing Unitree G1 USD asset fails
- Missing locomotion policy/controller fails
- Missing Isaac Sim / Isaac Lab fails
- Missing livestream support fails if `--live webrtc` is requested

Explicit fallback flags are required for development-only paths:

- `--allow-proxy`
- `--allow-kinematic-control`
- `--allow-rule-planner`

When used, these are printed and logged as non-primary development behavior.

## Repository Layout

```text
pathvla-unitree-isaac-live/
├── README.md
├── Makefile
├── .env.example
├── requirements-dev.txt
├── docker/
├── config/
├── pathvla/
├── isaac_ext/
├── apps/
├── scripts/
├── eval/
├── outputs/
└── tests/
```

## Prerequisites

- Ubuntu Linux VM with NVIDIA GPU
- `nvidia-smi` working
- Docker with NVIDIA container runtime
- Isaac Sim or Isaac Lab available via a compatible official base image or existing install
- Mac used only as remote client over SSH, browser, or Isaac livestream client

## Required Environment Variables

- `ISAAC_BASE_IMAGE`
- `VLA_ENDPOINT`
- `VLA_API_KEY` optional
- `VLA_MODEL_NAME` optional
- `UNITREE_G1_USD_PATH`
- `BREV_PUBLIC_HOST`
- `LIVESTREAM_PORTS`

Optional:

- `PATHVLA_OUTPUT_ROOT`
- `PATHVLA_API_HOST`
- `PATHVLA_API_PORT`
- `PATHVLA_DASHBOARD_PORT`

See [.env.example](/Users/kaushiksivakumar/workspace/robot-vla/pathvla-unitree-isaac-live/.env.example).

## Brev Setup

1. Create a Brev or equivalent Ubuntu GPU VM with NVIDIA drivers installed.
2. SSH from Mac into the VM.
3. Clone this repository.
4. Set environment variables.
5. Build the Isaac container.
6. Run the validation checks.

Commands:

```bash
bash scripts/setup_brev.sh
make check-gpu
make check-isaac
make check-livestream
make build
make live-demo
```

## Isaac Container Setup

This repo does not hardcode an Isaac image tag because NVIDIA image tags and access patterns change over time.

Set:

```bash
export ISAAC_BASE_IMAGE="<official-compatible-isaac-lab-or-isaac-sim-image>"
```

Examples depend on your NVIDIA entitlement and installation path. The Dockerfile uses:

```dockerfile
ARG ISAAC_BASE_IMAGE
FROM ${ISAAC_BASE_IMAGE}
```

You must supply a real Isaac-compatible base image.

## Live Viewing From Mac

### WebRTC / Isaac Livestream

Use:

```bash
make check-livestream
make live-demo
```

The system prints exact connection instructions including `BREV_PUBLIC_HOST` and the configured ports from [config/livestream.yaml](/Users/kaushiksivakumar/workspace/robot-vla/pathvla-unitree-isaac-live/config/livestream.yaml).

Open or forward the required ports on the VM. Then connect from the Mac using the Isaac WebRTC streaming client or the supported browser/client path documented by your Isaac build.

### Remote Desktop Alternative

Use `--live remote_desktop` and provision NICE DCV, VNC, or RDP separately. This path is documented, but it is not used as a silent fallback for broken livestream mode.

### Recorded Replay

Use:

```bash
make recorded-demo
```

This runs headless and records logs plus video when capture support is available.

## Main Strict Run On Brev

```bash
export VLA_ENDPOINT="https://your-vla-server/infer"
export UNITREE_G1_USD_PATH="/path/to/unitree_g1.usd"
export BREV_PUBLIC_HOST="<your-brev-host>"
export ISAAC_BASE_IMAGE="<official-compatible-isaac-lab-or-isaac-sim-image>"

make setup-brev
make check-gpu
make check-isaac
make check-livestream
make build
make live-demo
```

Expected outcome:

- Starts Isaac Sim or Isaac Lab
- Builds the selected room or warehouse scene
- Loads Unitree G1 asset
- Calls the real VLA endpoint
- Validates returned JSON
- Plans waypoints using live semantic scene state
- Executes movement in the Isaac simulation
- Exposes livestream for Mac viewing
- Records outputs under `outputs/`

## Development-Only Fallback Run

This remains a real Isaac Sim or Isaac Lab run, but it is not the primary claim.

```bash
make live-demo ALLOW_PROXY=1 ALLOW_KINEMATIC=1 ALLOW_RULE_PLANNER=1
```

This prints that:

- a proxy robot is being used instead of a real Unitree G1 asset
- kinematic control is being used instead of realistic locomotion
- rule planner mode is enabled instead of VLA mode

## API And Dashboard

Start the API:

```bash
make api
```

Start the Streamlit dashboard:

```bash
make dashboard
```

The dashboard controls real Isaac runs. It does not emulate simulation in the browser.

## Evaluation

Run the evaluation suite in recorded headless mode:

```bash
make eval
```

## Tests

Unit tests:

```bash
make test
```

Integration tests:

```bash
make integration-test
```

Integration tests require a configured Isaac environment and are marked with `pytest -m integration`.

## Troubleshooting

- `scripts/check_gpu.sh` fails: fix GPU driver or Docker NVIDIA runtime before anything else.
- `scripts/check_isaac.sh` fails: fix Isaac base image or host Isaac Python environment.
- `scripts/check_livestream.sh` fails: open the required ports and enable the supported Isaac streaming extensions.
- G1 asset missing: set `UNITREE_G1_USD_PATH` or rerun with `--allow-proxy`.
- No controller configured: provide a real controller config or rerun with `--allow-kinematic-control`.
- VLA invalid response: inspect `outputs/<run_id>/bad_vla_response.json`.
