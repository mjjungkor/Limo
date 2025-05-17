# ros2 param list
# ros2 param dump
# ros2 param dump turtlesim >> turtlesim.yaml
# ros2 run turtlesim turtlesim_node --ros-args --param-file turtlesim.yaml
# ros2 launch hello_ros2 moveTrutle.launch.py

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration # 대체가능한 입력이 가능하도록...
from ament_index_python import get_package_share_directory
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    param_dir=LaunchConfiguration(
        'param_dir', 
        default=os.path.join( # launch 시 yaml 변경하여 launch할 수 있도록 옵션 지정
            get_package_share_directory('hello_ros2'), 'param', 'turtlesim.yaml'
            ),
        ) 
    return LaunchDescription(
        [
            DeclareLaunchArgument('param_dir', default_value=param_dir, description='turtlesim parameter dump file',),
            Node(package='turtlesim', executable='turtlesim_node', parameters=[param_dir]),
            Node(package='hello_ros2', executable='move_turtle', parameters=[param_dir]),
            Node(package='hello_ros2', executable='change_color_client'),
        ]
    )