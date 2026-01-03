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

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, PythonExpression
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import PushRosNamespace
from launch.actions import GroupAction
from launch.conditions import IfCondition

def generate_launch_description():

    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_id",
            default_value="robot",
            description="Name for launch and config resources"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_model",
            default_value="anymal",
            description="URDF of the robot"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_xacro",
            default_value="anymal_d.urdf.xacro",
            description="URDF of the robot"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "use_sim",
            default_value="true",
            description="Enable simulation"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "headless_sim",
            default_value="false",
            description="Run simulation without graphical interface"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "world_sim",
            default_value="electrical_station.world",
            description="World for simulation"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_pose_x",
            default_value="0.0",
            description="Set the robot pose on the X axis"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_pose_y",
            default_value="0.0",
            description="Set the robot pose on the Y axis"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_pose_z",
            default_value="1.0",
            description="Set the robot pose on the Z axis"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_pose_a",
            default_value="0.0",
            description="Set the robot orientation in yaw"
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "run_rviz",
            default_value="false",
            description="Run Rviz gui"
        )
    )

    robot_id = LaunchConfiguration("robot_id")
    robot_model = LaunchConfiguration("robot_model")
    robot_xacro = LaunchConfiguration("robot_xacro")
    use_sim = LaunchConfiguration("use_sim")
    headless_sim = LaunchConfiguration("headless_sim")
    world_sim = LaunchConfiguration("world_sim")
    initial_pose_x = LaunchConfiguration("initial_pose_x")
    initial_pose_y = LaunchConfiguration("initial_pose_y")
    initial_pose_z = LaunchConfiguration("initial_pose_z")
    initial_pose_a = LaunchConfiguration("initial_pose_a") 
    run_rviz = LaunchConfiguration("run_rviz")

    robot_prefix = PythonExpression(["'", robot_id, "/'"])

    # Set the controllers configuration for ros2_controller
    controller_path = PathJoinSubstitution([
        FindPackageShare('quadruped_control'),
        'config/quadruped_controller.yaml'
    ])

    quadruped_locomotion_path = PathJoinSubstitution([
        FindPackageShare('quadruped_locomotion'),
        'config',
        'quadruped_drivers.yaml'
    ])

    # Set the parameters for hardware interface
    # use_sim = false -> Description package -> urdf -> Load config in ros2_control
    # use_sim = true  -> Description package -> urdf -> Not use config
    # hardware_path = PathJoinSubstitution([
    #     FindPackageShare('quadruped_hardware'),
    #     'config/hardware.yaml'
    # ])

    description = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('quadruped_description'), 'launch/description.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'use_sim': use_sim,
            'robot_model': robot_model,
            'robot_xacro': robot_xacro,
            #'controller_sim_path': controller_path, # Used for simulation
            #'hardware_path': hardware_path
        }.items()
    )

    control = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('quadruped_control'), 'launch/control.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'use_sim': use_sim,
            'controller_path': controller_path,
            'quadruped_locomotion_path': quadruped_locomotion_path
        }.items()
    )

    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('quadruped_gz_sim'), 'launch/simulation.launch.py'
            ])
        ),
        launch_arguments={
            'robot_id': robot_id,
            'robot_prefix': robot_prefix,
            'headless_sim': headless_sim,
            'world_sim': world_sim,
            'initial_pose_x': initial_pose_x,
            'initial_pose_y': initial_pose_y,
            'initial_pose_z': initial_pose_z,
            'initial_pose_a': initial_pose_a,
        }.items(),
        condition=IfCondition(use_sim)
    )

    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                 FindPackageShare('quadruped_description'), 'launch/rviz.launch.py'
            ])
        ),
        condition=IfCondition(run_rviz)
    )

    group = GroupAction([
        #PushRosNamespace(LaunchConfiguration('robot_id')),
        description,
        control,
        simulation,
        rviz
    ])

    return LaunchDescription(declared_arguments + [group])