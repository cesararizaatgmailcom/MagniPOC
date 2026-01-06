#!/usr/bin/env bash
set -euo pipefail

DURATION=${1:-120}
WORKSPACE_DIR="/home/ws"
MAPFILE="map.pbstream"

cd "$WORKSPACE_DIR"
source /opt/ros/jazzy/setup.bash || true
# If workspace built, source it
if [ -f "install/setup.bash" ]; then
  source install/setup.bash
fi

# Start simulation (Webots) in background
./scripts/launch-webots-simulation.sh &
SIM_PID=$!
sleep 6

# Start mapping
ros2 launch magni_mapping mapping.launch.py use_sim_time:=true &
MAP_PID=$!
sleep 5

# Start teleop for DURATION seconds to drive robot
./scripts/run-teleop-keyboard.sh &
TELEOP_PID=$!

sleep ${DURATION}

# Stop teleop
kill ${TELEOP_PID} || true
sleep 2

# Ask Cartographer to write state (pbstream)
if ros2 service list | grep -q '/write_state'; then
  ros2 service call /write_state cartographer_ros_msgs/srv/WriteState "{filename: '${MAPFILE}'}" || true
fi

# Basic sanity checks
# 1) pbstream file exists and non-empty
if [ ! -s "${MAPFILE}" ]; then
  echo "ERROR: ${MAPFILE} missing or empty"
  exit 2
fi

# 2) /map topic exists
if ! ros2 topic list | grep -q '/map'; then
  echo "ERROR: /map topic not present"
  exit 3
fi

# Optionally capture one message from /map (quick check)
ros2 topic echo /map -n 1 > /dev/null || true

# Teardown
kill ${MAP_PID} || true
kill ${SIM_PID} || true

echo "SMOKE TEST: OK - map saved to ${MAPFILE}"
exit 0
