#!/bin/bash

# Simple helper to launch the Webots simulation with optional features.
# Usage: ./launch-webots-simulation.sh [--rviz] [--mapping]

source /opt/ros/jazzy/setup.bash
source /home/ws/install/setup.bash

RVIZ=false
MAPPING=false

print_usage() {
  echo "Usage: $0 [--rviz] [--mapping]"
  echo
  echo "  --rviz       Launch RViz (default: false)"
  echo "  --mapping    Launch mapping subsystem (default: false)"
}

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --rviz)
      RVIZ=true
      shift
      ;;
    --mapping)
      MAPPING=true
      shift
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      print_usage
      exit 1
      ;;
  esac
done

LAUNCH_ARGS=()
if [ "$RVIZ" = true ]; then
  LAUNCH_ARGS+=("rviz:=true")
fi
if [ "$MAPPING" = true ]; then
  LAUNCH_ARGS+=("mapping:=true")
fi

# Launch the simulation (pass through chosen launch args)
ros2 launch magni_webots magni_sim_bringup.launch.py "${LAUNCH_ARGS[@]}"
