import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description() -> LaunchDescription:
		joy_config = launch.substitutions.LaunchConfiguration('joy_config')
    	publish_stamped_twist = launch.substitutions.LaunchConfiguration('publish_stamped_twist')
    	config_filepath = launch.substitutions.LaunchConfiguration('config_filepath')

		Arguments = [
		DeclareLaunchArgument('joy_vel', default_value='cmd_vel'),
        DeclareLaunchArgument('joy_config', default_value='ps3'),
        DeclareLaunchArgument('publish_stamped_twist', default_value='true'),
        DeclareLaunchArgument('config_filepath', default_value=[
            launch.substitutions.TextSubstitution(text=os.path.join(
                get_package_share_directory('teleop_twist_joy'), 'config', '')),
            joy_config, launch.substitutions.TextSubstitution(text='.config.yaml')]),
		]

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

		joy_linux_node = Node(
			package='joy_linux', executable='joy_linux_node', name='joy_linux_node'
		)

		teleop_twist_joy_node = Node(
            package='teleop_twist_joy', executable='teleop_node',
            name='teleop_twist_joy_node',
            parameters=[config_filepath, {'publish_stamped_twist': publish_stamped_twist}],
            remappings={('/cmd_vel', launch.substitutions.LaunchConfiguration('joy_vel'))},
		)

		ld = LaunchDescription(Arguments)
		ld.add_action(include_motors)
		ld.add_action(joy_linux_node)
		ld.add_action(teleop_twist_joy_node)
		return ld

