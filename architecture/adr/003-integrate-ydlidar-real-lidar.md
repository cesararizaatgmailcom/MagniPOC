# ADR 003 — Integrate YDLidar ROS2 Driver for Real Hardware LIDAR

Date: 2026-01-22

Status: Proposed

## Context
The MAGNI POC project currently supports simulated LIDAR via Webots for development and testing. To enable operation on real hardware, we need a ROS2 driver for the physical YDLidar sensor installed on the robot. The driver must publish LaserScan messages on the `/scan` topic with appropriate frame_id to integrate seamlessly with existing components like Cartographer 2D mapping.

## Decision
Integrate the `ydlidar_ros2_driver` package from the GitHub repository https://github.com/JAndresBP/ydlidar_ros2_driver/tree/humble into the workspace. Configure it for the specific YDLidar model used on MAGNI (to be determined; e.g., X4, G4, etc.), ensuring it publishes to `/scan` with `frame_id = "laser"` to match the simulation setup. Add conditional launching in `magni_bringup` to switch between simulated and real LIDAR based on a launch argument.

## Consequences
- Add `ydlidar_ros2_driver` as a new package in `src/`.
- Install YDLidar-SDK dependency as per the driver's README.
- Update `package.xml` in relevant packages to include dependencies.
- Modify `magni_bringup` launch files to include a `use_real_lidar` argument; when true, launch the YDLidar driver instead of relying on Webots simulation.
- Ensure TF tree includes the "laser" frame connected to "base_link".
- Update documentation and scripts to support real hardware testing.
- Potential need for serial port permissions and hardware-specific configurations on the robot platform.</content>
<parameter name="filePath">/home/ws/architecture/adr/003-integrate-ydlidar-real-lidar.md