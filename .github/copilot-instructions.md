# MAGNI POC Copilot Instructions

## Project Overview
This is a ROS2 (Jazzy) project implementing custom controllers for the Ubiquity Robotics MAGNI platform. Focuses on robot control, SLAM, navigation, and simulation using Webots. Key packages: `magni_description` (URDF), `magni_webots` (simulation), `ubiquity_motor_ros2` (motor hardware), `magni_bringup` (launch), `magni_mapping` (Cartographer 2D).

## Development Environment
- Use devcontainers (`.devcontainer/cpu-simulation` or `gpu-simulation`) for consistent ROS2 + Webots setup
- Workspace: `/home/ws` (matches `workspaceFolder` in devcontainer.json)
- Build: `colcon build --symlink-install` after sourcing `/opt/ros/jazzy/setup.bash`
- Source workspace: `source install/setup.bash`

## Key Workflows
- **Simulation**: `./scripts/launch-webots-simulation.sh [--rviz] [--mapping]` launches Webots with MAGNI
- **Teleop**: `./scripts/run-teleop-keyboard.sh` for keyboard control via `cmd_vel`
- **Build**: `./scripts/build-all.sh` builds all packages with specific base paths
- **Integration test**: `./scripts/run-integration-test.sh` validates core functionality

## Architecture Patterns
- **Launch files**: Python-based in `src/*/launch/`, use `DeclareLaunchArgument` for conditionals (e.g., `magni_sim_bringup.launch.py` with `rviz` and `mapping` args)
- **ros2_control**: Hardware plugins in `plugin_description.xml`, configs in `cfg/conf.yaml` (e.g., `ubiquity_velocity_controller` for diff drive)
- **Webots integration**: Plugins extend `webots_ros2_driver::PluginInterface`, registered in `*.xml` (e.g., `NodeRemover` removes caster joints)
- **URDF**: Xacro files in `src/magni_description/urdf/`, include `ros2_control` tags for hardware interfaces
- **Mapping**: Cartographer 2D with LIDAR (`/scan`) + odometry (`/odom`), configs in `src/magni_mapping/`

## Conventions
- **Topics**: Standard ROS2 (e.g., `cmd_vel`, `odom`, `scan`, `image_raw`)
- **Frames**: `base_link`, `odom`, `map` (Cartographer provides `map`)
- **Parameters**: YAML configs for controllers, launch args for features
- **Dependencies**: Managed via `rosdep`, listed in `package.xml`
- **Documentation**: Architecture decisions in `architecture/adr/`, designs in `architecture/`
- **Agents**: Use `ROS2Architect` for design/planning, `ROS2Developer` for implementation

## Common Patterns
- **Hardware interface**: Inherit `hardware_interface::SystemInterface`, implement read/write for joints
- **Launch includes**: Use `IncludeLaunchDescription` with `PythonLaunchDescriptionSource` and `IfCondition`
- **Plugin loading**: Export via `pluginlib` in CMakeLists.txt and XML description
- **Simulation time**: Set `use_sim_time:=true` in launch files for Webots
- **Config validation**: Check TF trees with `ros2 run tf2_tools view_frames`, topics with `ros2 topic list`

Reference: `architecture/baseline_architecture.md` for component overview, `README.md` for quick start.</content>
<parameter name="filePath">/home/ws/.github/copilot-instructions.md