# robot-vla

`robot-vla` contains `PathVLA Unitree Isaac Live`, a strict Isaac Sim / Isaac Lab project for running semantic navigation and task execution in a real NVIDIA GPU simulation environment.

The intended deployment target is a Linux cloud GPU VM such as Brev. The Mac is only a remote development and viewing client. This repo does not claim a local fake simulator, silent fallback planner, or pretend Unitree motion.

## Project

Main project directory:

- [pathvla-unitree-isaac-live](./pathvla-unitree-isaac-live/)

Primary project documentation:

- [Project README](./pathvla-unitree-isaac-live/README.md)

## What It Does

Given an instruction such as:

```text
Go to the red bin, avoid the chair, inspect the table, then return home.
```

the system is designed to:

- run Isaac Sim / Isaac Lab on a real NVIDIA GPU VM
- launch a real indoor room or warehouse scene
- load a real Unitree G1 USD asset, or fail unless explicit proxy mode is allowed
- call a real VLA HTTP endpoint, or fail unless explicit debug-only rule planning is allowed
- validate returned subgoals with a strict schema
- plan waypoints in the live Isaac scene state
- execute motion in simulation
- expose livestream or remote viewing options
- record video, logs, traces, and results

## Strictness

Default behavior is intentionally strict:

- no mocked VLA by default
- no fake local Mac simulator
- no silent substitution of missing Isaac or robot assets
- no implicit kinematic fallback

Development-only flags exist, but they must be passed explicitly and are logged as non-primary behavior.

## Quick Start

On the target GPU VM:

```bash
cd pathvla-unitree-isaac-live
bash scripts/setup_brev.sh
make check-gpu
make check-isaac
make check-livestream
make build
make live-demo
```

Required environment variables include:

- `ISAAC_BASE_IMAGE`
- `VLA_ENDPOINT`
- `UNITREE_G1_USD_PATH`
- `BREV_PUBLIC_HOST`

See the full setup guide in the [Project README](./pathvla-unitree-isaac-live/README.md).

## Repo Notes

- Root-level `.gitignore` excludes virtualenvs, outputs, and generated frames.
- Runtime outputs are written under `pathvla-unitree-isaac-live/outputs/`.
- Unit and integration tests live under `pathvla-unitree-isaac-live/tests/`.
