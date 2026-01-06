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

Smoke test script: `scripts/run-mapping-smoke-test.sh` (invoked by CI and can be run locally).
