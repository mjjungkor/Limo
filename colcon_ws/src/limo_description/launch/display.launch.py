# ros2 param list
# ros2 param dump
# ros2 param dump turtlesim >> turtlesim.yaml
# ros2 run turtlesim turtlesim_node --ros-args --param-file turtlesim.yaml
# ros2 launch hello_ros2 moveTrutle.launch.py

# sudo apt install ros-humble-urdf-launch
# ros2 launch limo_description display.launch.py

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution # 대체가능한 입력이 가능하도록...
from ament_index_python import get_package_share_directory
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    default_model_path=PathJoinSubstitution(['urdf','myfirst.urdf'])
    model= DeclareLaunchArgument(name='model', default_value=default_model_path, description='myfirst urdf file')
    return LaunchDescription(
        [
            model,
            Node(package='hello_ros2', executable='move_turtle'),
            #Node(package='hello_ros2', executable='action_client'),
            IncludeLaunchDescription(
                PathJoinSubstitution(
                    [FindPackageShare('urdf_launch'), 'launch', 'display.launch.py']),
                launch_arguments={
                    'urdf_package':'limo_description',
                    'urdf_package_path':LaunchConfiguration('model'),}
                    .items(),
            ),
        ]
    )