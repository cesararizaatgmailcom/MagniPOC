"""Launch file for Magni bringup.

This launch description includes the `ubiquity_motor_ros2` motors launch and
starts a teleop node. Which teleop node is launched is controlled by the
`use_joystick_teleop` launch argument (boolean). By default the keyboard
teleop (`teleop_twist_keyboard`) is used. The teleop nodes are started with a
`stamped` parameter so they publish stamped Twist messages by default.

Examples
--------
Launch with default keyboard teleop (stamped True):
	ros2 launch magni_bringup magni_bringup.launch.py

Launch with joystick teleop:
	ros2 launch magni_bringup magni_bringup.launch.py use_joystick_teleop:=true

Override stamped parameter at launch time:
	ros2 launch magni_bringup magni_bringup.launch.py stamped:=false
"""

from __future__ import annotations

import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description() -> LaunchDescription:
		"""Generate the launch description for magni bringup.

		Declares two launch arguments:
		- use_joystick_teleop: boolean, defaults to false. If true, starts joystick
			teleop (teleop_twist_joy). If false (default) starts keyboard teleop
			(teleop_twist_keyboard).
		- stamped: boolean, defaults to true. Passed as the `stamped` parameter to
			the teleop node so it can publish stamped Twist messages.
		"""

		use_joy = LaunchConfiguration('use_joystick_teleop')
		stamped = LaunchConfiguration('stamped')

		declare_use_joy = DeclareLaunchArgument(
				'use_joystick_teleop', default_value='false',
				description='If true start joystick teleop, otherwise keyboard teleop (default)'
		)

		declare_stamped = DeclareLaunchArgument(
				'stamped', default_value='true',
				description='Whether teleop should publish stamped Twist messages (true/false)'
		)

		# Include the motors launch from ubiquity_motor_ros2
		ubiq_share = get_package_share_directory('ubiquity_motor_ros2')
		motors_launch_path = os.path.join(ubiq_share, 'launch', 'motors.launch.py')
		include_motors = IncludeLaunchDescription(
				PythonLaunchDescriptionSource(motors_launch_path)
		)

		# Joystick teleop (started when use_joystick_teleop == true)
		joy_node = Node(
				package='teleop_twist_joy',
				executable='teleop_node',
				name='teleop_twist_joy',
				output='screen',
				parameters=[{'stamped': stamped}],
				condition=IfCondition(use_joy),
		)

		ld = LaunchDescription()
		ld.add_action(declare_use_joy)
		ld.add_action(declare_stamped)
		ld.add_action(include_motors)
		ld.add_action(joy_node)

		return ld

