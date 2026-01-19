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
- Mapping launch should allow starting with: `ros2 launch magni_bringup magni_bringup.launch.py enable_mapping:=true` (or run `ros2 launch magni_mapping mapping.launch.py`).
- Provide remappings or parameter overrides for topic names if the Webots-URDF driver uses non-standard names.

## Specialized Task Patterns — Cartographer Debugging & Integration
This section collects practical patterns and checks extracted from common Cartographer integration tasks.

### Launch configuration
- Prefer passing `-configuration_directory <abs-path>` and `-configuration_basename <file>` via launch arguments (avoid ROS1 `$(find ...)` substitutions in YAML)
- Validate the launch supplies the correct param file and `use_sim_time` consistently

### Configuration validation
- Verify top-level options in your Lua file: `map_frame`, `tracking_frame`, `published_frame`, `odom_frame`, `provide_odom_frame`, `use_odometry`, `use_nav_sat`, `use_landmarks`
- Check trajectory builder params: `min_range`, `max_range`, `num_accumulated_range_data`, `use_imu_data`, `submaps.num_range_data`
- Confirm `MAP_BUILDER.num_background_threads` is tuned for available CPU resources
- Reference: https://google-cartographer-ros.readthedocs.io/en/latest/configuration.html

### TF & frame troubleshooting
- **Self-transform (`TF_SELF_TRANSFORM`)**: ensure `published_frame != odom_frame`. If `provide_odom_frame=true`, Cartographer publishes `odom_frame -> published_frame`.
- **Frame unreachability**: verify the TF chain `sensor -> body_frame -> tracking_frame -> odom -> map` is complete
- Use `ros2 run tf2_tools view_frames.py` to visualize the TF graph and `ros2 topic echo /scan` to confirm `frame_id`
- Ensure `robot_state_publisher` (URDF static TFs) launches before odometry and Cartographer to avoid race conditions

### Common patterns
- Odometry-only (no IMU): `tracking_frame = "base_footprint"`, `use_imu_data = false`
- External odometry: `use_odometry = true`, `provide_odom_frame = true`
- If scan frame name is `laser` or `laser_link`, ensure URDF attaches that link to the body frame (fixed joint)

### Quick checks
- `ros2 param list /cartographer_node` and `ros2 param get /cartographer_node configuration_directory`
- `ros2 topic echo /scan --once | grep frame_id`
- `ros2 run tf2_tools view_frames.py` (open frames.pdf)

(Adapted from the project agent guidance; keep this section in the architecture docs for reference and extension.)

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