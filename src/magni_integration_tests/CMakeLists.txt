cmake_minimum_required(VERSION 3.8)
project(magni_integration_tests)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_ros REQUIRED)
find_package(launch REQUIRED)
find_package(launch_ros REQUIRED)
find_package(launch_testing REQUIRED)
find_package(launch_testing_ament_cmake REQUIRED)
find_package(rclpy REQUIRED)

if(BUILD_TESTING)
  find_package(ament_cmake_ros REQUIRED)
  find_package(launch_testing_ament_cmake REQUIRED)

  function(add_ros_isolated_launch_test path)
    set(RUNNER "${ament_cmake_ros_DIR}/run_test_isolated.py")
    add_launch_test("${path}" RUNNER "${RUNNER}" ${ARGN})
  endfunction()

  # Register integration tests
  add_ros_isolated_launch_test(test/test_mapping_integration.py)
endif()

ament_package()
