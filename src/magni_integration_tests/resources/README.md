Place a rosbag containing robot movement commands (topics used to drive the robot in simulation) in this folder named `drive.bag`.

Example:
- `drive.bag` should replay the cmd_vel / odom / joint_state topics expected by the simulation and mapping stack.

Note: tests will be skipped if the bag file is not present. This allows CI to opt-in to run the test when an appropriate bag is available.