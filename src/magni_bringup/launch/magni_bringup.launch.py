import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description() -> LaunchDescription:
		
		# Include the motors launch from ubiquity_motor_ros2
		ubiq_share = get_package_share_directory('ubiquity_motor_ros2')
		motors_launch_path = os.path.join(ubiq_share, 'launch', 'motors.launch.py')
		include_motors = IncludeLaunchDescription(
				PythonLaunchDescriptionSource(motors_launch_path)
		)

		teleop_twist_joy_pkg_share = get_package_share_directory('teleop_twist_joy')
		teleop_twist_joy_launch = os.path.join(
			teleop_twist_joy_pkg_share,
			'launch',
			'teleop-launch.py'
		)

		teleop_twist_joy_include = IncludeLaunchDescription(
			PythonLaunchDescriptionSource(teleop_twist_joy_launch),
			launch_arguments={
				'joy_config': 'ps3',
				'publish_stamped_twist': 'True'
			}.items()
		)

		ld = LaunchDescription()
		ld.add_action(include_motors)
		ld.add_action(teleop_twist_joy_include)
		return ld

