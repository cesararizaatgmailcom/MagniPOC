import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_output = LaunchConfiguration('map_output', default='map.pbstream')

    pkg_share = get_package_share_directory('magni_mapping')

    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        output='screen',
        parameters=[os.path.join(pkg_share, 'params', 'cartographer_params.yaml'), {'use_sim_time': use_sim_time}],
        remappings=[('/scan', '/scan'), ('/odom', '/odom')]
    )

    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        output='screen',
        parameters=[os.path.join(pkg_share, 'params', 'cartographer_params.yaml'), {'use_sim_time': use_sim_time}],
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('map_output', default_value='map.pbstream'),
        cartographer_node,
        occupancy_grid_node,
    ])
