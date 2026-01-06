# Cartographer Integration Design (MAGNI POC)

## Decision summary
- Mapping mode: **2D** (Cartographer 2D)
- Sensors: **LIDAR + Odometry** (no IMU required for initial integration)
- Initial target: **simulation (Webots)**; later port to real robot with serial motor HW and odometry verified

## Rationale
- MAGNI has a planar LIDAR (topic `/scan`) and reliable wheel odometry (`/odom`) from `ubiquity_velocity_controller`; 2D mapping is simpler, well-supported by Cartographer, and fits available sensors.
- Simulation-first reduces risk, allows safe tuning, and supports automated smoke tests before hardware deployment.

## Required topics & frames
- Laser: `sensor_msgs/msg/LaserScan` → topic: `/scan` (from URDF/Webots) 
- Odometry: `nav_msgs/msg/Odometry` → topic: `/odom` (controller publishes odom)
- TF frames:
  - `base_link` (robot frame)
  - `odom` (odometry frame; produced by wheel odometry)
  - `map` (Cartographer provides this)
- Use `use_sim_time := true` in simulation

## Config & files to add (recommended layout)
- New package: **`magni_mapping`** (or add under `magni_bringup` if preferred)
  - `config/magni_2d.lua` — Cartographer configuration (map_frame, odom_frame, scan matcher params, range limits)
  - `config/magni_urdf_tf.lua` — small helper if needed for frame configuration
  - `launch/mapping.launch.py` — starts `cartographer_node` and `cartographer_occupancy_grid_node` with `use_sim_time` argument and remappings
  - `params/cartographer_params.yaml` — overrides tuned parameters (e.g., `num_point_clouds`, `min_range`, `max_range`, `max_trajectory_length`, `submaps/` size)
  - `README.md` — instructions to run mapping, known caveats

## Key Cartographer parameters to tune (initial suggestions)
- use_odometry = true
- use_imu = false
- submaps/num_range_data = 90 (tune based on scan frequency)
- scan_matcher/translation_weight, rotation_weight (lower if odom is good)
- min_range / max_range based on LIDAR spec in URDF xacro

## Launch & integration notes
- Ensure `use_sim_time` is propagated to all nodes when running in Webots.
- Mapping launch should allow starting with: `ros2 launch magni_bringup mapping.launch.py use_sim_time:=true` (or run `mapping.launch.py` from `magni_mapping`).
- Provide remappings or parameter overrides for topic names if the Webots-URDF driver uses non-standard names.

## Smoke test (simulation) — acceptance criteria
1. Start Webots simulation (`./scripts/launch-webots-simulation.sh`) with mapping launch added in a second terminal.
2. Teleop robot for ~60–120s (use `./scripts/run-teleop-keyboard.sh`).
3. Verify Cartographer publishes `/map` and `map->odom` transform; generate a pbstream or occupancy grid file.
4. Basic metric: map contains obstacles and free space (manual check), and `map` coverage increases as robot moves.

## Risks & follow-ups
- If odometry is noisy, consider integrating IMU or enabling scan-only SLAM parameters and tighter loop closure settings.
- When moving to hardware: ensure correct serial/odometry timestamping and TF alignment; carefully test odometry scaling and covariance.

---

Ready to proceed with creating config templates and a mapping package when you give the go-ahead.