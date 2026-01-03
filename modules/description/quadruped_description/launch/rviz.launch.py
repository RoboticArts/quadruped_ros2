from launch_ros.actions import Node
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.actions import GroupAction

def generate_launch_description():

    rviz_config_path = PathJoinSubstitution([
        FindPackageShare('quadruped_description'),
        'config/rviz.rviz'
    ])

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]
    )

    group = GroupAction([
        rviz
    ])

    return LaunchDescription([group])