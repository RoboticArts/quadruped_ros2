from launch.actions import RegisterEventHandler, GroupAction, LogInfo
from launch_ros.actions import Node, PushRosNamespace
from launch import LaunchDescription
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition

def generate_launch_description():

    robot_id = LaunchConfiguration("robot_id")
    robot_prefix = LaunchConfiguration("robot_prefix")
    use_sim = LaunchConfiguration("use_sim")
    controller_path = LaunchConfiguration("controller_path")
    quadruped_locomotion_path = LaunchConfiguration("quadruped_locomotion_path")

    ros2_control = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[controller_path],
        output="both",
    )

    # Run joint_state_broadcaster controller
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
        ],
    )

    # Run robot_base_controller controller
    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "robot_base_controller",
        ]
    )

    robot_controller_spawner_after_joint_state = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[
                GroupAction([
                    # We need to redeclare PushRosNamespace here because event handlers (like OnProcessExit)
                    # do not automatically inherit the namespace from the parent launch scope
                    # PushRosNamespace(robot_id), OJOOOOOOOOOOOOOOOOOOO 
                    LogInfo(msg='joint_state_broadcaster spawned, spawning robot_controller'),
                    robot_controller_spawner
                ])
            ],
        )
    )

    quadruped_locomotion = Node(
        package="quadruped_locomotion",
        executable="quadruped_locomotion",
        arguments=['--driver-config', quadruped_locomotion_path],
        output="screen",
    )

    group = GroupAction([
        ros2_control,
        joint_state_broadcaster_spawner,
        robot_controller_spawner_after_joint_state,
        quadruped_locomotion
    ])

    return LaunchDescription([group])