include "map_builder.lua"
include "trajectory_builder_2d.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER_2D,
  map_frame = "map",
  tracking_frame = "base_link",
  published_frame = "odom",
  odom_frame = "odom",
  provide_odom_frame = true,
  use_odometry = true,
  use_nav_sat = false,
  use_landmarks = false,
  publish_tracked_pose = true,
  pose_publish_period_sec = 0.05,
  trajectory_publish_period_sec = 0.01,
  rangefinder_sampling_ratio = 1.0,
  odometry_sampling_ratio = 1.0,
  imu_sampling_ratio = 1.0,
}

-- Trajectory builder params (tune as needed)
TRAJECTORY_BUILDER_2D.min_range = 0.1
TRAJECTORY_BUILDER_2D.max_range = 30.0
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 5.0
TRAJECTORY_BUILDER_2D.num_accumulated_range_data = 1

-- Submaps
MAP_BUILDER.num_background_threads = 4
TRAJECTORY_BUILDER_2D.submaps.num_range_data = 90

-- Use odometry and disable IMU for now
TRAJECTORY_BUILDER_2D.use_imu_data = false

return options
