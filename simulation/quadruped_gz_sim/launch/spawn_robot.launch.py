from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import GroupAction
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    robot_name = LaunchConfiguration("robot_name", default="anymal")
    initial_pose_x = LaunchConfiguration("initial_pose_x", default="0.0")
    initial_pose_y = LaunchConfiguration("initial_pose_y", default="0.0")
    initial_pose_z = LaunchConfiguration("initial_pose_z", default="1.0")
    initial_pose_a = LaunchConfiguration("initial_pose_a", default="0.0")           

    gazebo_spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', [robot_id, '/', robot_name], # Robot name for Gazebo world
            '-topic', "robot_description",
            '-x', initial_pose_x,
            '-y', initial_pose_y,
            '-z', initial_pose_z,
            '-Y', initial_pose_a,
        ],
        output='screen',
    )

    bridge_config = PathJoinSubstitution([
        FindPackageShare('quadruped_gz_sim'),
        'config/bridge.yaml'
    ])

    gazebo_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[
            {'config_file': bridge_config},
        ],
    )

    group = GroupAction([
        gazebo_spawn,
        gazebo_bridge
    ])

    return LaunchDescription([group])