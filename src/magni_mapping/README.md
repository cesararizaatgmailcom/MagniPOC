magni_mapping — Cartographer 2D (LIDAR + Odometry)

This package contains: 
- Cartographer configs (`config/magni_2d.lua`)
- ROS2 params (`params/cartographer_params.yaml`)
- Launch file (`launch/mapping.launch.py`)

Run (simulation):
```
# in devcontainer
colcon build --symlink-install
source install/setup.bash
# start mapping (after starting Webots):
ros2 launch magni_mapping mapping.launch.py use_sim_time:=true
```

Smoke test/integration test: `magni_integration_tests` package (tests rely on a `drive.bag` resource placed in `src/magni_integration_tests/resources/drive.bag`). The CI runs this integration test to exercise mapping in simulation.
## Notes & Tuning 🔧
- Use `ros2 launch magni_bringup magni_bringup.launch.py enable_mapping:=true` to launch mapping as part of the robot bringup; alternatively, run `ros2 launch magni_mapping mapping.launch.py use_sim_time:=true` directly for standalone mapping.
- Save a pbstream (map) on demand with `./scripts/save_pbstream.py --filename my_map.pbstream` after the mapping run completes (script calls `/write_state`).
- Tuning tips:
  - Start with `TRAJECTORY_BUILDER_2D.num_accumulated_range_data = 1` and `submaps.num_range_data = 90` and adjust if scans are dropped.
  - Set `TRAJECTORY_BUILDER_2D.min_range` and `max_range` to match your sensor's spec (see `magni_2d.lua`).
  - Keep IMU disabled for LIDAR+odometry workflow unless you have reliable IMU data.

## Quick Acceptance Checklist ✅
- `colcon build` succeeds with `magni_mapping` included.
- `ros2 launch magni_bringup magni_bringup.launch.py enable_mapping:=true` starts Cartographer and publishes `/map` and the `map->odom` TF (or run `ros2 launch magni_mapping mapping.launch.py`).
- The pbstream can be written via `/write_state` and resulting file is non-empty.