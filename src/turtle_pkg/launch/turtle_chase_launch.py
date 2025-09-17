from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    config=os.path.join(get_package_share_directory('turtle_pkg'),'config','params.yaml')

    return LaunchDescription([
        Node(package='turtlesim',executable='turtlesim_node',name='sim'),
        Node(package='turtle_pkg',executable='turtle_chase',name='turtle_chase',parameters=[config])
    ])