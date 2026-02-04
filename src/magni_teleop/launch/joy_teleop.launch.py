import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description() -> LaunchDescription:
    """
    Launch file for joystick teleop control using joy_linux and teleop_twist_joy.
    
    This launch file launches:
    - joy_linux_node: Reads joystick input and publishes Joy messages
    - teleop_twist_joy_node: Converts Joy messages to Twist commands
    """
    
    joy_config = LaunchConfiguration('joy_config')
    publish_stamped_twist = LaunchConfiguration('publish_stamped_twist')
    config_filepath = LaunchConfiguration('config_filepath')
    joy_vel = LaunchConfiguration('joy_vel')

    arguments = [
        DeclareLaunchArgument(
            'joy_vel',
            default_value='cmd_vel',
            description='Target velocity topic for joystick commands'
        ),
        DeclareLaunchArgument(
            'joy_config',
            default_value='ps3',
            description='Joystick configuration type (ps3, xbox, logitech, etc.)'
        ),
        DeclareLaunchArgument(
            'publish_stamped_twist',
            default_value='true',
            description='Whether to publish stamped twist messages'
        ),
        DeclareLaunchArgument(
            'config_filepath',
            default_value=[
                TextSubstitution(
                    text=os.path.join(
                        get_package_share_directory('teleop_twist_joy'),
                        'config',
                        ''
                    )
                ),
                joy_config,
                TextSubstitution(text='.config.yaml')
            ],
            description='Path to joystick configuration file'
        ),
    ]

    # Joy Linux node - reads joystick input from /dev/input/js*
    joy_linux_node = Node(
        package='joy_linux',
        executable='joy_linux_node',
        name='joy_linux_node',
        output='screen'
    )

    # Teleop Twist Joy node - converts joy messages to cmd_vel
    teleop_twist_joy_node = Node(
        package='teleop_twist_joy',
        executable='teleop_node',
        name='teleop_twist_joy_node',
        output='screen',
        parameters=[config_filepath, {'publish_stamped_twist': publish_stamped_twist}],
        remappings=[('/cmd_vel', joy_vel)],
    )

    ld = LaunchDescription(arguments)
    ld.add_action(joy_linux_node)
    ld.add_action(teleop_twist_joy_node)

    return ld
