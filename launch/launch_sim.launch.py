import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node



def generate_launch_description():



    package_name='holonomic' 

    # Get the package directory
    pkg_path = get_package_share_directory(package_name)

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    pkg_path,'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

    # Add static transform publisher for odom to world
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher',
        output='screen',
        arguments=['0', '0', '0',  # translation: x, y, z
                  '0', '0', '0',   # rotation: roll, pitch, yaw
                  'world',         # parent frame
                  'odom']          # child frame
    )

    # Include RViz
    rviz = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    pkg_path, 'launch', 'rviz.launch.py'
                )])
    )

    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        static_tf,
        rviz
    ])
