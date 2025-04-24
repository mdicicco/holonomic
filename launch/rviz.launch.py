import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    pkg_path = os.path.join(get_package_share_directory('holonomic'))
    rviz_config_path = os.path.join(pkg_path, 'rviz','default.rviz')


    start_rviz2 = Node(package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]
    )
	
    return LaunchDescription([
        start_rviz2
    ])
