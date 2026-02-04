# YDLidar ROS2 Driver Integration Design (MAGNI POC)

## Decision summary
- Driver: **ydlidar_ros2_driver** from https://github.com/JAndresBP/ydlidar_ros2_driver/tree/humble
- Target: **Real hardware** (complements existing Webots simulation)
- Configuration: Conditional launching based on `use_real_lidar` argument in bringup

## Rationale
- MAGNI uses a YDLidar sensor for real-world operation; the ROS2 driver provides native support for publishing LaserScan messages.
- Integration allows seamless switching between simulation (Webots) and hardware, maintaining the same `/scan` topic and `laser` frame_id for compatibility with Cartographer and other components.
- Follows project patterns: add as a new package, integrate via launch arguments in `magni_bringup`.

## Required topics & frames
- LaserScan: `sensor_msgs/msg/LaserScan` → topic: `/scan` (driver publishes)
- TF frames:
  - `laser` (sensor frame; matches simulation URDF)
  - Connected via fixed joint to `base_link` in URDF
- Services: `start_scan`, `stop_scan` (for control if needed)

## Config & files to add (recommended layout)
- New package: **`ydlidar_ros2_driver`** (clone from GitHub into `src/`)
  - Use the humble branch for ROS2 compatibility.
- In `magni_bringup`:
  - Update launch files to add `use_real_lidar` argument (default: false)
  - When true, include YDLidar launch; when false, rely on Webots.
- Parameter file: `params/ydlidar_<model>.yaml` (e.g., for X4, G4) with `frame_id: "laser"`, port, baudrate, etc.
- Ensure YDLidar-SDK is installed as per README.

## Key YDLidar parameters to tune (initial suggestions)
- port: /dev/ttyUSB0 (or appropriate serial port)
- frame_id: "laser"
- baudrate: 230400 (model-specific)
- lidar_type: 1 (TRIANGLE)
- angle_min/max: -180.0 / 180.0
- range_min/max: 0.01 / 64.0 (adjust based on model)
- frequency: 10.0 Hz
- auto_reconnect: true

## Launch & integration notes
- Install YDLidar-SDK: Clone and build https://github.com/YDLIDAR/YDLidar-SDK
- Add dependency in `magni_bringup/package.xml` if needed.
- Modify `magni_bringup.launch.py` to conditionally launch `ydlidar_launch.py` with `IfCondition(use_real_lidar)`
- Ensure serial permissions: May need `sudo chmod 777 /dev/ttyUSB*` or udev rules.
- For hardware: Set `use_sim_time := false`

## Specialized Task Patterns — YDLidar Debugging & Integration
This section collects practical patterns for integrating and troubleshooting YDLidar.

### Driver setup
- Confirm YDLidar-SDK is installed and linked correctly (check CMake errors).
- Verify serial port: `ls /dev/ttyUSB*` and permissions.
- Test standalone: `ros2 launch ydlidar_ros2_driver ydlidar_launch.py` and check `/scan`.

### Configuration validation
- Match `lidar_type` and `device_type` to your model (see params/*.yaml examples).
- Ensure `frame_id` matches URDF (e.g., "laser").
- Check angle and range limits against sensor spec.

### TF & topic troubleshooting
- Confirm `/scan` publishes with correct `frame_id`.
- Verify TF: `laser` should be child of `base_link` (fixed joint in URDF).
- Use `ros2 topic echo /scan --once` to inspect message.

### Common patterns
- Serial connection: `device_type: 0`, `port: /dev/ttyUSB0`
- Network (if applicable): `device_type: 1` or `2`, adjust port.
- Intensity: Enable if sensor supports and needed for mapping.

### Quick checks
- `ros2 topic list | grep scan`
- `ros2 topic hz /scan`
- `ros2 run tf2_tools view_frames.py` (check laser frame)

## Smoke test (hardware) — acceptance criteria
1. Connect YDLidar to robot, ensure power and serial connection.
2. Launch bringup with `use_real_lidar:=true`.
3. Verify `/scan` publishes at expected rate (e.g., 10 Hz).
4. Check TF tree includes `laser` frame.
5. Integrate with Cartographer: Enable mapping and confirm SLAM works.

## Risks & follow-ups
- Hardware-specific: Serial port may vary; ensure correct model params.
- Permissions: May require sudo or udev rules for serial access.
- Compatibility: Test with ROS2 Jazzy (driver is humble-based).
- Performance: Ensure driver doesn't overload CPU on robot hardware.</content>
<parameter name="filePath">/home/ws/architecture/ydlidar_integration_design.md