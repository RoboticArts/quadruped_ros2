from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.conditions import UnlessCondition

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    headless_sim = LaunchConfiguration("headless_sim")
    world_sim = LaunchConfiguration("world_sim")

    world_path = PathJoinSubstitution([
        FindPackageShare('quadruped_gz_worlds'),
        'worlds',
        world_sim
    ])

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
            ])
        ),
        launch_arguments={
            'gz_args': ['-r ', '-s ',  world_path],
            'on_exit_shutdown': 'true'
        }.items(),
    )

    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'), 'launch/gz_sim.launch.py'
            ])
        ),
        launch_arguments={
            'gz_args': ['-g'],
            'on_exit_shutdown': 'true'
        }.items(),
        condition=UnlessCondition(headless_sim)
    )

    group = GroupAction([
        gazebo_server,
        gazebo_client,
    ])

    return LaunchDescription([group])