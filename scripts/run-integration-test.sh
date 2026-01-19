#!/bin/bash

source /opt/ros/jazzy/setup.bash
source install/setup.bash

colcon test --ctest-args tests --packages-select magni_integration_tests