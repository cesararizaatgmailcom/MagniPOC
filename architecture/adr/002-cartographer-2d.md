# ADR 002 — Cartographer 2D for MAGNI (LIDAR + Odometry)

Date: 2026-01-06

Status: Accepted

## Context
We need a reliable 2D SLAM solution for MAGNI. The robot has a 2D LIDAR and wheel odometry. We aim for a simulation-first approach (Webots) to tune parameters before running on hardware.

## Decision
Adopt Cartographer 2D using LIDAR + odometry (IMU disabled by default). Start with simulation and tune `magni_2d.lua` parameters such as `min_range`, `max_range`, `num_accumulated_range_data`, and submap sizes.

## Consequences
- Mapping launch and configs live under `src/magni_mapping`.
- `magni_bringup` exposes an `enable_mapping` launch argument to include mapping as part of bringup.
- pbstreams saved via `/write_state` provide reproducible map snapshots for deployment.
- IMU remains optional; enable only if odometry is insufficient.

