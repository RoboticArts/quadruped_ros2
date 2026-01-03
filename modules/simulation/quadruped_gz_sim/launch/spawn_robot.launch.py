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