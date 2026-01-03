# Copyright 2026, Robert Vasquez Zavaleta.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
        parameters=[
          controller_path,
          {"use_sim_time": use_sim},
        ],
        output="both",
    )

    # Run joint_state_broadcaster controller
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
        ],
        parameters=[{"use_sim_time": use_sim}]
    )

    # Run robot_base_controller controller
    robot_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "robot_base_controller",
        ],
        parameters=[{"use_sim_time": use_sim}]
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