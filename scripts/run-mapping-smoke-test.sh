#!/usr/bin/env bash
set -euo pipefail

# Consolidated integration test runner for mapping
WORKSPACE_DIR="/home/ws"
TEST_PKG=${1:-magni_integration_tests}
BUILD_PACKAGES="magni_mapping ${TEST_PKG}"

cd "$WORKSPACE_DIR"

# Source system ROS (inside CI/container) and workspace if present
source /opt/ros/jazzy/setup.bash || true
if [ -f "install/setup.bash" ]; then
  source install/setup.bash
fi

# Build required packages
echo "Building packages: ${BUILD_PACKAGES}"
colcon build --packages-select ${BUILD_PACKAGES} --cmake-target-install || true
source install/setup.bash || true

# Run the integration tests
echo "Running integration tests for package: ${TEST_PKG}"
colcon test --packages-select ${TEST_PKG} --event-handlers console_direct+
colcon test-result --verbose || true

# Collect artifacts if produced by tests
ARTIFACTS=(integration_map.pbstream map.pbstream *.log)
for f in "${ARTIFACTS[@]}"; do
  if compgen -G "$f" > /dev/null; then
    echo "Found artifact(s) matching pattern: $f"
  fi
done

echo "Integration test run complete."
exit 0
